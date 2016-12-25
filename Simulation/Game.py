import random

from Drawing.Maps import Map


class Game:
    def __init__(self):
        self.map = Map()
        self.out_roads = [self.map.top.first, self.map.right.first,
                          self.map.bottom.first, self.map.left.first]

    def update(self):
        self.__update_out()
        self.__update_in()
        return [self.map]

    def __update_out(self):
        for road in self.out_roads:
            for lane in road:
                for i in range(len(lane) - 1, 0, -1):
                    lane[i] = lane[i - 1]
                lane[0] = self.__pull_car(self.out_roads.index(road) - 1)

    def __update_in(self):
        in_roads = [self.map.top.second, self.map.right.second, self.map.bottom.second, self.map.left.second]
        for road in in_roads:
            direction = in_roads.index(road)
            for lane in road:
                if self.__is_green():
                    if lane[-1] == 1:
                        self.__push_car(direction)
                    for i in range(len(lane) - 1, 0, -1):
                        lane[i] = lane[i - 1]
                    lane[0] = self.__generate_car(direction)

    def __pull_car(self, direction=0):
        return random.choice([0 for _ in range(direction + 3)] + [1])

    def __push_car(self, direction=0):
        print('car_pushed ', direction)

    def __generate_car(self, direction):
        return random.choice([0, 0, 0, 0, 1]) if direction == 0 else 0
        # return random.choice([0 for _ in range(direction + 3)] + [1])

    def __is_green(self, source=0, destination=0):
        return True
