import random

from Drawing.Maps import Map


class Game:
    def __init__(self, screen):
        self.map = Map()
        self.screen = screen
        self.out_roads = [self.map.top.first,
                          self.map.right.first,
                          self.map.bottom.first,
                          self.map.left.first]

    def update(self):
        self.update_out()
        self.update_in()
        self.update_view()

    def update_out(self):
        for road in self.out_roads:
            for lane in road:
                for i in range(len(lane) - 1, 0, -1):
                    lane[i] = lane[i - 1]
                lane[0] = self.pull_car(self.out_roads.index(road) - 1)

    def update_in(self):
        in_roads = [self.map.top.second, self.map.right.second, self.map.bottom.second, self.map.left.second]
        for road in in_roads:
            for lane in road:
                if self.is_green():
                    for i in range(len(lane) - 1, 0, -1):
                        lane[i] = lane[i - 1]
                    lane[0] = self.generate_car(in_roads.index(road))
                    self.push_car()

    def pull_car(self, direction=0):
        return random.choice([0 for _ in range(direction + 3)] + [1])

    def push_car(self, direction=0):
        pass

    def generate_car(self, direction):
        return random.choice([0 for _ in range(direction + 3)] + [1])

    def is_green(self, source=0, destination=0):
        return True

    def update_view(self):
        self.map.prepare(self.screen)
        self.map.draw(self.screen)
