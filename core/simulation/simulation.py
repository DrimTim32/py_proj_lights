"""This file contains simulation class"""
from data_structures import str_to_direction, Orientation, Directions, TurnDirection
from drawing.maps import create_map_painter
from .data_collector import DataCollector
from .intersection import Intersection, IntersectionProperties
from .lights_managers.lights_phase import LightsPhase, DirectionsInfo
from .road import RoadSizeVector, get_empty_road


class Simulation:
    def __init__(self, car_generator, lights_manager, config):
        self.__data_collector = DataCollector()

        self.__probabilities = Simulation.___create_probability_info(config.directions_turns)

        self.__lanes_info = Simulation.__create_lanes_info(config.directions_turns)

        self.__car_generator = car_generator(self.__probabilities)

        self.__lights_manager = lights_manager(Simulation.create_lights_phases(config.directions_turns),
                                               self.__lanes_info)

        self.__roads, self.__intersection = Simulation.__create_roads_and_intersection(config.directions_lanes,
                                                                                       config.roads_length)

        self.__map = create_map_painter(self.__intersection, self.__roads)

    def update(self):
        """Updates whole object"""
        self.__update_out()
        self.__intersection.update()
        self.__lights_manager.update()
        self.__update_in()
        # print(self.__lights_manager.current_phase)
        # print(self.__data_collector.data)

    def __update_out(self):
        for direction_str in self.__roads.keys():
            direction = str_to_direction(direction_str)
            road = self.__roads[direction_str]
            road.update_out()
            for lane_index in range(road.out_width):
                road.push_car_out(lane_index, self.__intersection.pull_car(direction, lane_index))

    def __update_in(self):
        for direction_str in self.__roads.keys():
            road = self.__roads[direction_str]
            direction = str_to_direction(direction_str)
            for lane_index in range(road.in_width):
                if self.__is_safe_passage(direction, lane_index):
                    if road.has_waiting_car(lane_index):
                        car = road.pull_car(lane_index)
                        self.__data_collector.register(car, lane_index, self.__lights_manager.current_phase)
                        self.__intersection.push_car(direction, lane_index, car)
                road.update_in(lane_index)
                road.push_car_in(lane_index, self.__car_generator.generate(direction, lane_index))

    def get_number_of_phases(self):
        """
        :return:number of lights phases
        :rtype: int
        """
        return len(self.__lights_manager.phases)

    def set_phases_durations(self, new_durations):
        """
        sets new duration of lights phases
        :param new_durations: new durations
        :type new_durations: list[int]
        :return: none
        """
        for phase_id in range(len(self.__lights_manager.phases)):
            phase = self.__lights_manager.phases[phase_id]
            phase.duration = new_durations[phase_id]

    def get_lights(self):
        lights = {Directions.TOP: [],
                  Directions.LEFT: [],
                  Directions.BOTTOM: [],
                  Directions.RIGHT: []}
        for direction in lights.keys():
            for lane_index in range(self.__roads[direction.__str__()].in_width):
                lights[direction].append(self.__lights_manager.is_green(direction, lane_index))
        return lights

    def __is_safe_passage(self, direction, lane_index):
        is_green = self.__lights_manager.is_green(direction, lane_index)
        current_phase = self.__lights_manager.phases[self.__lights_manager.current_phase]
        if not current_phase.left:
            return is_green
        if current_phase.left and not self.__lanes_info[direction][lane_index].left:
            return is_green
        else:
            phase_time = current_phase.duration
            op_dir = Directions((direction + 2) % 4)
            weight = sum(self.__probabilities[direction][lane_index])
            op_weight = 0
            for lane_index in range(len(self.__lanes_info[op_dir])):
                if self.__lanes_info[op_dir][lane_index].left:
                    op_weight += sum(self.__probabilities[op_dir][lane_index])
            w_sum = weight + op_weight
            weight = weight / w_sum
            op_weight = op_weight / w_sum
            time = int(weight * phase_time)
            op_time = int(op_weight * phase_time)
            if direction in [0, 1]:
                my_turn = self.__lights_manager.in_phase_time <= time
            else:
                my_turn = self.__lights_manager.in_phase_time > op_time

            if my_turn:
                return my_turn and is_green
            else:
                turn = self.__roads[direction.__str__()].first_waiting_car_turn(lane_index)
                if turn is None:
                    return is_green
                else:
                    return is_green and turn == TurnDirection.RIGHT

    @property
    def top(self):
        """Top roads"""
        return self.__roads["top"]

    @property
    def right(self):
        """Right roads"""
        return self.__roads["right"]

    @property
    def left(self):
        """Left roads"""
        return self.__roads["left"]

    @property
    def bottom(self):
        """Bottom roads"""
        return self.__roads["bottom"]

    @property
    def map(self):
        """
        :return:  map
        :rtype: MapPainter
        """
        return self.__map

    @property
    def points(self):
        """Returns all points [top, left, bottom, right]"""
        return [self.top, self.left, self.bottom, self.right]

    @property
    def current_data(self):
        """
        :return: data collected by simulation
        :rtype: dict[list[LanePhaseData]]
        """
        return self.__data_collector.data

    @staticmethod
    def __create_roads_and_intersection(directions_lanes, roads_length):
        """
        :param directions_lanes: information about number of lanes
        :param roads_length: roads length
        :return: roads and intersection
        :rtype: dict[str, Road], Intersection
        """
        directions_properties = [None, None, None, None]
        for direction_id in directions_lanes.keys():
            direction = directions_lanes[direction_id]
            directions_properties[direction_id] = RoadSizeVector(roads_length,
                                                                 direction[1],
                                                                 direction[0])

        roads = {"top": get_empty_road(directions_properties[0]),
                 "left": get_empty_road(directions_properties[1]),
                 "bottom": get_empty_road(directions_properties[2]),
                 "right": get_empty_road(directions_properties[3])}

        return roads, Intersection(IntersectionProperties(directions_properties))

    @staticmethod
    def create_lights_phases(directions_turns):
        """
        :param directions_turns: information about directions
        :return: lights phases
        :rtype: list[LightsPhase]
        """
        phases = []
        for direction_id in directions_turns.keys():
            direction = directions_turns[direction_id]
            for lane in direction:
                turns = Simulation.check_turns(lane)
                phase = LightsPhase(DirectionsInfo(turns[0], turns[1], turns[2], turns[3]),
                                    Simulation.__check_orientation(direction_id), 20)
                is_new_phase = True
                for existing_phase_id in range(len(phases)):
                    if phase == phases[existing_phase_id]:
                        phases[existing_phase_id] += phase
                        is_new_phase = False
                        break
                if is_new_phase:
                    phases.append(phase)
        # print(phases)
        return phases

    @staticmethod
    def __create_lanes_info(directions_turns=None):
        """
        :param directions_turns: information about directions
        :return: lanes info
        :rtype: dict[Directions, list[DirectionsInfo]]
        """
        lanes_info = {Directions.TOP: [],
                      Directions.LEFT: [],
                      Directions.BOTTOM: [],
                      Directions.RIGHT: []}
        for direction_id in directions_turns.keys():
            direction = directions_turns[direction_id]
            for lane in direction:
                turns = Simulation.check_turns(lane)
                lanes_info[Directions(direction_id)].append(
                    DirectionsInfo(turns[0], turns[1], turns[2], turns[3]))
        return lanes_info

    @staticmethod
    def check_turns(lane):
        """
        :param lane: lane data from config
        :return: possible turn direction from lane
        :rtype: list[bool]
        """
        turns = [False, False, False, False]
        for turn_direction in lane.keys():
            if turn_direction == 3 and lane[turn_direction][1]:
                turns[3] = True
            else:
                turns[turn_direction - 1] = True
        return turns

    @staticmethod
    def ___create_probability_info(directions_turns):
        """
        :param directions_turns: information about directions
        :return: probabilities for car generation
        :rtype: dict[Directions,list[list[float]]]
        """
        probabilities = {Directions.TOP: [],
                         Directions.LEFT: [],
                         Directions.BOTTOM: [],
                         Directions.RIGHT: []}
        for direction_id in directions_turns.keys():
            direction = directions_turns[direction_id]
            for lane in direction:
                direction_probabilities = probabilities[Directions(direction_id)]
                direction_probabilities.append([0, 0, 0])
                lane_probabilities = direction_probabilities[-1]
                for turn_direction in lane.keys():
                    lane_probabilities[turn_direction - 1] = lane[turn_direction][0]
        # print(probabilities)
        return probabilities

    @staticmethod
    def __check_orientation(direction):
        """
        :param direction: checks orientation of given direction
        :type direction: Direction
        :return: orientation
        :rtype: Orientation
        """
        return Orientation(direction % 2)
