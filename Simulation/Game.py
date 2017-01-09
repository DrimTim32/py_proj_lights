from Drawing.Maps import Map
from Simulation.Intersection import *
from Simulation.Road import *


class Game:
    def __init__(self, car_generator, lights_manager):
        self.car_generator = car_generator
        self.lights_manager = lights_manager

        directions = [
            RoadSizeVector(8, 2, 3),  # top
            RoadSizeVector(8, 2, 2),  # left
            RoadSizeVector(8, 2, 2),  # bottom
            RoadSizeVector(8, 2, 2)  # right
        ]
        self.roads = {
            "top": get_empty_road(directions[0]),
            "left": get_empty_road(directions[1]),
            "bottom": get_empty_road(directions[2]),
            "right": get_empty_road(directions[3])
        }

        self.intersection = Intersection(IntersectionProperties(directions))

        self.map = Map(self.intersection, self.roads)

        self.out_roads = [self.top.out_lanes, self.right.out_lanes,
                          self.bottom.out_lanes, self.left.out_lanes]
        self.in_roads = [self.top.in_lanes, self.right.in_lanes,
                         self.bottom.in_lanes, self.left.in_lanes]

    def update(self):
        self.lights_manager.update()
        self.__update_out()
        self.__update_in()
        return [self.map]

    def __update_out(self):
        for direction in range(len(self.roads)):
            road = self.out_roads[direction]
            for lane in road:
                for i in range(len(lane) - 1, 0, -1):
                    lane[i] = lane[i - 1]
                lane[0] = self.intersection.pull_car(direction, road.index(lane))

    def __update_in(self):
        for direction in range(len(self.in_roads)):
            road = self.in_roads[direction]
            for lane in road:
                if self.lights_manager.is_green(direction, lane):
                    if lane[-1] == 1:
                        self.intersection.push_car(direction, road.index(lane))
                    for i in range(len(lane) - 1, 0, -1):
                        lane[i] = lane[i - 1]
                    lane[0] = self.car_generator.generate(direction, road.index(lane))

    @property
    def top(self):
        return self.roads["top"]

    @property
    def right(self):
        return self.roads["right"]

    @property
    def left(self):
        return self.roads["left"]

    @property
    def bottom(self):
        return self.roads["bottom"]
