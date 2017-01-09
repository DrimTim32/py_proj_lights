from Drawing.Maps import Map
from Simulation.DataStructures.IntersectionProperties import *
from Simulation.Intersection import *
from Simulation.Road import *


class Game:
    def __init__(self, car_generator, lights_manager):
        self.car_generator = car_generator
        self.lights_manager = lights_manager
        vectors = [
            RoadSizeVector(8, 2, 3),  # top
            RoadSizeVector(8, 2, 2),  # left
            RoadSizeVector(8, 2, 2),  # bottom
            RoadSizeVector(8, 2, 2)  # right
        ]
        self.roads = {
            "top": get_empty_road(vectors[0]),
            "down": get_empty_road(vectors[2]),
            "left": get_empty_road(vectors[1]),
            "right": get_empty_road(vectors[3])
        }
        self.map = Map(vectors, self.roads)

        dimensions = IntersectionProperties([
            DirectionProperties(2, 3),  # top
            DirectionProperties(2, 2),  # left
            DirectionProperties(2, 2),  # bottom
            DirectionProperties(2, 2)  # right
        ])

        self.intersection = Intersection(dimensions)
        self.out_roads = [self.map.top.out_lanes, self.map.right.out_lanes,
                          self.map.bottom.out_lanes, self.map.left.out_lanes]
        self.in_roads = [self.map.top.in_lanes, self.map.right.in_lanes,
                         self.map.bottom.in_lanes, self.map.left.in_lanes]

    def update(self):
        self.lights_manager.update()
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
                if self.lights_manager.is_green(direction, lane):
                    if lane[-1] == 1:
                        self.intersection.push_car(direction, road.index(lane))
                    for i in range(len(lane) - 1, 0, -1):
                        lane[i] = lane[i - 1]
                    lane[0] = self.car_generator.generate(direction, road.index(lane))
