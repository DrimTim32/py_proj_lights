
from core.simulation.enums import Directions

class IntersectionProperties:
    def __init__(self, directions):
        self.top = directions[0]
        self.left = directions[1]
        self.bottom = directions[2]
        self.right = directions[3]
        self.directions = directions
        self.width = max(self.top.in_lanes_count + self.top.out_lanes_count,
                         self.bottom.in_lanes_count + self.bottom.out_lanes_count)
        self.height = max(self.left.in_lanes_count + self.left.out_lanes_count,
                          self.right.in_lanes_count + self.right.out_lanes_count)


class Intersection:
    def __init__(self, properties):
        self.array = [[0 for _ in range(properties.width)] for _ in range(properties.height)]
        self.width = properties.width
        self.height = properties.height

    def update(self):
        pass

    def push_car(self, direction, lane, car):
        if direction == Directions.TOP:
            self.array[0][lane] = car
        elif direction == Directions.LEFT:
            self.array[self.height - 1 - lane][0] = car
        elif direction == Directions.BOTTOM:
            self.array[self.height - 1][self.width - lane - 1] = car
        else:  # RIGHT
            self.array[lane][self.width - 1] = car

    def pull_car(self, direction, lane):
        ret = 0
        if direction == Directions.TOP and self.__check_pull_top(lane):
            ret = self.array[0][self.width - lane - 1]
            self.array[0][self.width - lane - 1] = 0
        elif direction == Directions.LEFT and self.__check_pull_left(lane):
            ret = self.array[lane][0]
            self.array[lane][0] = 0
        elif direction == Directions.BOTTOM and self.__check_pull_bottom(lane):
            ret = self.array[self.height - 1][lane]
            self.array[self.height - 1][lane] = 0
        elif direction == Directions.RIGHT and self.__check_pull_right(lane):
            ret = self.array[self.height - 1 - lane][self.width - 1]
            self.array[self.height - 1 - lane][self.width - 1] = 0
        return ret

    def __check_pull_top(self, lane):
        on_field = self.array[0][self.width - lane - 1]
        if on_field != 0 and on_field.destination == Directions.TOP:
            return True
        return False

    def __check_pull_left(self, lane):
        on_field = self.array[lane][0]
        if on_field != 0 and on_field.destination == Directions.LEFT:
            return True
        return False

    def __check_pull_bottom(self, lane):
        on_field = self.array[self.height - 1][lane]
        if on_field != 0 and on_field.destination == Directions.BOTTOM:
            return True
        return False


    def __check_pull_right(self, lane):
        on_field = self.array[self.height - 1 - lane][self.width - 1]
        if on_field != 0 and on_field.destination == Directions.RIGHT:
            return True
        return False
