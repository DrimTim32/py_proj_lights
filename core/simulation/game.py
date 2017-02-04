from core.data_structures.road import RoadSizeVector, get_empty_road
from core.drawing.maps import create_map_painter
from core.simulation.enums import str_to_direction
from core.simulation.intersection import Intersection, IntersectionProperties


class Game:
    def __init__(self, car_generator, lights_manager):
        self.__car_generator = car_generator
        self.__lights_manager = lights_manager

        directions = [
            RoadSizeVector(8, 2, 2),  # top
            RoadSizeVector(8, 2, 2),  # left
            RoadSizeVector(8, 2, 2),  # bottom
            RoadSizeVector(8, 2, 2)  # right
        ]
        self.__roads = {
            "top": get_empty_road(directions[0]),
            "left": get_empty_road(directions[1]),
            "bottom": get_empty_road(directions[2]),
            "right": get_empty_road(directions[3])
        }

        self.__intersection = Intersection(IntersectionProperties(directions))

        self.__map = create_map_painter(self.__intersection, self.__roads)

    @property
    def points(self):
        """Returns all points [top, left, bottom, right]"""
        return [self.top, self.left, self.bottom, self.right]

    def update(self):
        """Updates whole object"""
        self.__lights_manager.update()
        self.__update_out()
        self.__intersection.update()
        self.__update_in()

    def __update_out(self):
        for direction in self.__roads.keys():
            road = self.__roads[direction]
            road.update_out()
            for lane_index in range(road.out_width):
                road.push_car(lane_index, self.__intersection.pull_car(str_to_direction(direction), lane_index))

    def __update_in(self):
        for direction in self.__roads.keys():
            road = self.__roads[direction]
            for lane_index in range(road.in_width):
                lane = road[lane_index]
                if self.__lights_manager.is_green(str_to_direction(direction), lane_index):
                    if lane[-1] != 0:
                        self.__intersection.push_car(str_to_direction(direction), lane_index, lane[-1])
                        lane[-1] = 0
                    for i in range(len(lane) - 1, 0, -1):
                        if lane[i] == 0:
                            lane[i] = lane[i - 1]
                            lane[i - 1] = 0
                    if lane[0] == 0:
                        lane[0] = self.__car_generator.generate(str_to_direction(direction), lane_index)

    def calculate_offset(self, direction):
        pass

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
        return self.__map
