from core.data_structures.enums import str_to_direction, Orientation
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

        self.__lights_manager = lights_manager(Simulation.__create_lights_phases(), self.__lanes_info)

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
    def __create_lights_phases(turns=None):
        return [LightsPhase(DirectionsInfo(True, True, False, False), Orientation.VERTICAL, 20),
                LightsPhase(DirectionsInfo(False, False, False, True), Orientation.VERTICAL, 20),
                LightsPhase(DirectionsInfo(True, True, False, False), Orientation.HORIZONTAL, 20),
                LightsPhase(DirectionsInfo(False, False, False, True), Orientation.HORIZONTAL, 20)]

    @staticmethod
    def __create_lanes_info(turns=None):
        return {"top": [DirectionsInfo(True, True, False, False), DirectionsInfo(False, False, False, True)],
                "left": [DirectionsInfo(True, True, False, False), DirectionsInfo(False, False, False, True)],
                "bottom": [DirectionsInfo(True, True, False, False), DirectionsInfo(False, False, False, True)],
                "right": [DirectionsInfo(True, True, False, False), DirectionsInfo(False, False, False, True)]}
