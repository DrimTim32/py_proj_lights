import random

from Drawing.DataStructures.Road import RoadSizeVector
from Drawing.Maps import Map
from Simulation.DataStructures.IntersectionProperties import *
from Simulation.Intersection import *


class Game:
    def __init__(self):
        self.map = Map([
            RoadSizeVector(8, 2, 2),  # top
            RoadSizeVector(8, 2, 2),  # left
            RoadSizeVector(8, 2, 2),  # bottom
            RoadSizeVector(8, 2, 2)  # right
        ])

        dimensions = IntersectionProperties([
            DirectionProperties(2, 2),  # top
            DirectionProperties(2, 2),  # left
            DirectionProperties(2, 2),  # bottom
            DirectionProperties(2, 2)  # right
        ])

        self.intersection = Intersection(dimensions)
        self.out_roads = [self.map.top.first, self.map.right.first,
                          self.map.bottom.first, self.map.left.first]
        self.in_roads = [self.map.top.second, self.map.right.second,
                         self.map.bottom.second, self.map.left.second]

    def update(self):
        self.__update_out()
        self.__update_in()
        return [self.map]

    def __update_out(self):
        for direction in range(len(self.out_roads)):
            road = self.out_roads[direction]
            for lane in road:
                for i in range(len(lane) - 1, 0, -1):
                    lane[i] = lane[i - 1]
                lane[0] = self.intersection.pull_car(direction, road.index(lane))

    def __update_in(self):
        for direction in range(len(self.in_roads)):
            road = self.in_roads[direction]
            for lane in road:
                if self.__is_green():
                    if lane[-1] == 1:
                        self.intersection.push_car(direction, road.index(lane))
                    for i in range(len(lane) - 1, 0, -1):
                        lane[i] = lane[i - 1]
                    lane[0] = self.__generate_car(direction, road.index(lane))

    def __generate_car(self, direction, lane=0):
        return random.choice([0, 0, 0, 0, 1]) if direction == 0 else 0
        # return random.choice([0 for _ in range(direction + 3)] + [1])

    def __is_green(self, source=0, destination=0):
        return True
