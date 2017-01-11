from core.simulation import Car
from core.simulation.enums import Directions, TurnDirection


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
        self.properties = properties

    def update(self):
        self.__update_right()
        self.__update_straight()
        self.__update_left()

    def __update_right(self):
        # top left quarter
        for row in range(self.properties.left.out_lanes_count - 1, -1, -1):
            for col in range(self.properties.top.in_lanes_count):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if row < col:
                        self.array[row + 1][col] = on_field
                    else:
                        self.array[row][col - 1] = on_field
                    self.array[row][col] = 0

        # bottom left quarter
        for col in range(self.properties.bottom.out_lanes_count - 1, -1, -1):
            for row in range(self.height - 1, self.height - 1 - self.properties.left.in_lanes_count, -1):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.height - row > self.properties.bottom.out_lanes_count - col:
                        self.array[row + 1][col] = on_field
                    else:
                        self.array[row][col + 1] = on_field
                    self.array[row][col] = 0

        # bottom right quarter
        for row in range(self.height - self.properties.right.out_lanes_count, self.height):
            for col in range(self.width - 1, self.width - 1 - self.properties.bottom.in_lanes_count, -1):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.height - row < self.width - col:
                        self.array[row - 1][col] = on_field
                    else:
                        self.array[row][col + 1] = on_field
                    self.array[row][col] = 0

        # top right quarter
        for col in range(self.width - self.properties.bottom.out_lanes_count, self.width):
            for row in range(self.properties.right.in_lanes_count):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.properties.right.in_lanes_count - row < self.width - col:
                        self.array[row - 1][col] = on_field
                    else:
                        self.array[row][col - 1] = on_field
                    self.array[row][col] = 0

    def __update_straight(self):
        orientation = self.__check_orientation()
        if orientation is None:
            return

        if orientation == 0:  # vertical
            # left half

            # right half

            pass
        else:  # horizontal
            # top half

            # bottom half

            pass

        for row in range(self.properties.left.out_lanes_count - 1, -1, -1):
            for col in range(self.properties.top.in_lanes_count):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    self.array[row][col] = 0

        # bottom left quarter
        for col in range(self.properties.bottom.out_lanes_count - 1, -1, -1):
            for row in range(self.height - 1, self.height - 1 - self.properties.left.in_lanes_count, -1):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    self.array[row][col] = 0

        # bottom right quarter
        for row in range(self.height - self.properties.right.out_lanes_count, self.height):
            for col in range(self.width - 1, self.width - 1 - self.properties.bottom.in_lanes_count, -1):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    self.array[row][col] = 0

        # top right quarter
        for col in range(self.width - self.properties.bottom.out_lanes_count, self.width):
            for row in range(self.properties.right.in_lanes_count):
                on_field = self.array[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    self.array[row][col] = 0

    def __update_left(self):
        # TODO
        pass

    def __check_orientation(self):
        for row in self.array:
            for cell in row:
                if isinstance(cell, Car):
                    return cell.source % 2
        return None

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
        if isinstance(on_field, Car) and on_field.destination == Directions.TOP:
            return True
        return False

    def __check_pull_left(self, lane):
        on_field = self.array[lane][0]
        if isinstance(on_field, Car) and on_field.destination == Directions.LEFT:
            return True
        return False

    def __check_pull_bottom(self, lane):
        on_field = self.array[self.height - 1][lane]
        if isinstance(on_field, Car) and on_field.destination == Directions.BOTTOM:
            return True
        return False

    def __check_pull_right(self, lane):
        on_field = self.array[self.height - 1 - lane][self.width - 1]
        if isinstance(on_field, Car) and on_field.destination == Directions.RIGHT:
            return True
        return False
