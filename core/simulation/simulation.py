from core.data_structures.enums import str_to_direction, Orientation, Directions
from core.drawing.maps import create_map_painter
from core.simulation.data_collector import DataCollector
from core.simulation.intersection import Intersection, IntersectionProperties
from core.simulation.lights_managers.lights_phase import LightsPhase, DirectionsInfo
from core.simulation.road import RoadSizeVector, get_empty_road


class Simulation:
    def __init__(self, car_generator, lights_manager, config):
        self.__data_collector = DataCollector()

        self.__lanes_info = Simulation.__create_lanes_info(config.directions_turns)

        self.__car_generator = car_generator(self.__lanes_info)

        self.__lights_manager = lights_manager(Simulation.__create_lights_phases(config.directions_turns),
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
        for direction in self.__roads.keys():
            road = self.__roads[direction]
            road.update_out()
            for lane_index in range(road.out_width):
                road.push_car_out(lane_index, self.__intersection.pull_car(str_to_direction(direction), lane_index))

    def __update_in(self):
        for direction in self.__roads.keys():
            road = self.__roads[direction]
            for lane_index in range(road.in_width):
                if self.__lights_manager.is_green(str_to_direction(direction), lane_index):
                    if road.has_waiting_car(lane_index):
                        car = road.pull_car(lane_index)
                        self.__data_collector.register(car, lane_index, self.__lights_manager.current_phase)
                        self.__intersection.push_car(str_to_direction(direction), lane_index, car)
                road.update_in(lane_index)
                road.push_car_in(lane_index, self.__car_generator.generate(str_to_direction(direction), lane_index))

    def calculate_offset(self, direction):
        pass

    def set_lights_phases(self, new_phases):
        self.__lights_manager.phases = new_phases

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
    def __create_lights_phases(directions_turns):
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
                phases.append(LightsPhase(DirectionsInfo(turns[0], turns[1], turns[2], turns[3]),
                                          Simulation.__check_orientation(direction_id), 20))
        return phases

    @staticmethod
    def __create_lanes_info(directions_turns=None):
        """
        :param directions_turns: information about directions
        :return: lanes info
        :rtype: dict[str, list[DirectionsInfo]]
        """
        lanes_info = {"top": [],
                      "left": [],
                      "bottom": [],
                      "right": []}
        for direction_id in directions_turns.keys():
            direction = directions_turns[direction_id]
            for lane in direction:
                turns = Simulation.check_turns(lane)
                lanes_info[Directions(direction_id).__str__()].append(
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
    def create_probability_info(directions_turns):
        """
        :param directions_turns: information about directions
        :return: probabilities for car generation
        :rtype: dict[str,list[list[float]]]
        """
        pass

    @staticmethod
    def __check_orientation(direction):
        """
        :param direction: checks orientation of given direction
        :type direction: Direction
        :return: orientation
        :rtype: Orientation
        """
        return Orientation(direction % 2)
