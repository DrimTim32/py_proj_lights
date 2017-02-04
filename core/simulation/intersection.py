"""
File containing Intersection class and supporting tools
"""

from core.simulation.car import Car
from core.simulation.enums import Directions, TurnDirection


class IntersectionProperties:
    """
    Class handling properties of intersection
    """

    def __init__(self, directions):
        """
        initializes intersection proeprties from roads properties
        :param directions: array of properties of roads
        :type directions: list[RoadSizeVector]
        """
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
    """
    Intersection class
    """

    def __init__(self, properties):
        """
        Initialzes Intersection from properties
        :param properties: properties of intersection
        :type properties: IntersectionProperties
        """
        self.__array_upper = [[0 for _ in range(properties.width)] for _ in range(properties.height)]
        self.__array_lower = [[0 for _ in range(properties.width)] for _ in range(properties.height)]
        self.__width = properties.width
        self.__height = properties.height
        self.__properties = properties

    def update(self):
        """
        Updates positions of cars on intersection
        :return: none
        """
        self.__update_right()
        self.__update_straight()
        self.__update_left()

    def __update_right(self):
        """
        updates positions of cars turning right
        :return: none
        """
        # top left quarter
        for row in range(self.__properties.left.out_lanes_count - 1, -1, -1):
            for col in range(self.__properties.top.in_lanes_count):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if row < col:
                        self.__array_upper[row + 1][col] = on_field
                    else:
                        self.__array_upper[row][col - 1] = on_field
                    self.__array_upper[row][col] = 0

        # bottom left quarter
        for col in range(self.__properties.bottom.out_lanes_count - 1, -1, -1):
            for row in range(self.__height - 1, self.__height - 1 - self.__properties.left.in_lanes_count, -1):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.__height - row > self.__properties.bottom.out_lanes_count - col:
                        self.__array_upper[row + 1][col] = on_field
                    else:
                        self.__array_upper[row][col + 1] = on_field
                    self.__array_upper[row][col] = 0

        # bottom right quarter
        for row in range(self.__height - self.__properties.right.out_lanes_count, self.__height):
            for col in range(self.__width - 1, self.__width - 1 - self.__properties.bottom.in_lanes_count, -1):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.__height - row < self.__width - col:
                        self.__array_upper[row - 1][col] = on_field
                    else:
                        self.__array_upper[row][col + 1] = on_field
                    self.__array_upper[row][col] = 0

        # top right quarter
        for col in range(self.__width - self.__properties.bottom.out_lanes_count, self.__width):
            for row in range(self.__properties.right.in_lanes_count):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.__properties.right.in_lanes_count - row < self.__width - col:
                        self.__array_upper[row - 1][col] = on_field
                    else:
                        self.__array_upper[row][col - 1] = on_field
                    self.__array_upper[row][col] = 0

    def __update_straight(self):
        """
        updates positions of cars going straight
        :return: none
        """
        orientation = self.__check_orientation()
        if orientation is None:
            return

        if orientation == 0:  # vertical
            # left half
            for row in range(self.__height - 1, -1, - 1):
                for col in range(self.__properties.top.in_lanes_count):
                    on_field = self.__array_upper[row][col]
                    if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                        print(row, col)
                        self.__array_upper[row + 1][col] = on_field
                        self.__array_upper[row][col] = 0

            # right half
            for row in range(self.__height):
                for col in range(self.__width - self.__properties.bottom.in_lanes_count, self.__width):
                    on_field = self.__array_upper[row][col]
                    if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                        self.__array_upper[row - 1][col] = on_field
                        self.__array_upper[row][col] = 0

        else:  # horizontal
            # top half
            for col in range(self.__width):
                for row in range(self.__properties.right.in_lanes_count):
                    on_field = self.__array_upper[row][col]
                    if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                        self.__array_upper[row][col - 1] = on_field
                        self.__array_upper[row][col] = 0

            # bottom half
            for col in range(self.__width - 1, -1, -1):
                for row in range(self.__height - self.__properties.left.in_lanes_count, self.__height):
                    on_field = self.__array_upper[row][col]
                    if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                        self.__array_upper[row][col + 1] = on_field
                        self.__array_upper[row][col] = 0

    def __update_left(self):
        """
        updates positions of cars turning left
        :return: none
        """
        orientation = self.__check_orientation()
        if orientation is None:
            return

        if orientation == 0:  # vertical
            in_lane_base = self.__properties.top.in_lanes_count - 1
            for i in range(self.__properties.right.out_lanes_count):
                on_field = self.__array_upper[0][in_lane_base - i]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 0:
                    self.__array_upper[self.__height - self.__properties.right.out_lanes_count + i][
                        self.__width - 1] = on_field
                    self.__array_upper[0][in_lane_base - i] = 0

            in_lane_base = self.__width - self.__properties.bottom.in_lanes_count
            for i in range(self.__properties.left.out_lanes_count):
                on_field = self.__array_lower[self.__height - 1][in_lane_base + i]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 2:
                    self.__array_lower[self.__properties.left.out_lanes_count - 1 - i][0] = on_field
                    self.__array_lower[self.__height - 1][in_lane_base + i] = 0

        else:  # horizontal
            in_lane_base = self.__properties.right.in_lanes_count - 1
            for i in range(self.__properties.bottom.out_lanes_count):
                on_field = self.__array_upper[in_lane_base - i][self.__width - 1]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 3:
                    self.__array_upper[self.__height - 1][self.__properties.bottom.out_lanes_count - 1 - i] = on_field
                    self.__array_upper[in_lane_base - i][self.__width - 1] = 0

            in_lane_base = self.__height - self.__properties.left.in_lanes_count
            for i in range(self.__properties.top.out_lanes_count):
                on_field = self.__array_lower[in_lane_base + i][0]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 1:
                    self.__array_lower[0][self.__width - self.__properties.top.out_lanes_count + i] = on_field
                    self.__array_lower[in_lane_base + i][0] = 0

    def __check_orientation(self):
        """
        Checks orientation of current lights phase
        :return: orientation or none
        :rtype int, None
        """
        for row in self.__array_upper:
            for cell in row:
                if isinstance(cell, Car):
                    return cell.source % 2
        return None

    def push_car(self, direction, lane, car):
        """
        Adds car from road to the intersection
        :param direction: direction from which car is arriving
        :param lane: lane from which car is ariving
        :param car: Car
        :type direction: Directions
        :type lane: int
        :type car: Car
        :return: none
        """
        if direction == Directions.TOP:
            self.__array_upper[0][lane] = car
        elif direction == Directions.LEFT:
            if car.turn_direction == TurnDirection.LEFT:
                self.__array_lower[self.__height - 1 - lane][0] = car
            else:
                self.__array_upper[self.__height - 1 - lane][0] = car
        elif direction == Directions.BOTTOM:
            if car.turn_direction == TurnDirection.LEFT:
                self.__array_lower[self.__height - 1][self.__width - lane - 1] = car
            else:
                self.__array_upper[self.__height - 1][self.__width - lane - 1] = car
        else:  # RIGHT
            self.__array_upper[lane][self.__width - 1] = car

    def pull_car(self, direction, lane, offset=0):
        """
        Removes car from intersection and returns it
        :param direction: direction in which car is going
        :param lane: lane in which car is going
        :param offset: offset between lanes on intersection and lanes on road
        :type direction: Directions
        :type lane: int
        :type offset: int
        :return: car
        :rtype: Car
        """
        ret = 0
        if direction == Directions.TOP and self.__check_pull_top(lane):
            ret = self.__array_upper[0][self.__width - lane - 1]
            self.__array_upper[0][self.__width - lane - 1] = 0
        elif direction == Directions.LEFT and self.__check_pull_left(lane):
            ret = self.__array_upper[lane][0]
            self.__array_upper[lane][0] = 0
        elif direction == Directions.BOTTOM and self.__check_pull_bottom(lane):
            ret = self.__array_upper[self.__height - 1][lane]
            self.__array_upper[self.__height - 1][lane] = 0
        elif direction == Directions.RIGHT and self.__check_pull_right(lane):
            ret = self.__array_upper[self.__height - 1 - lane][self.__width - 1]
            self.__array_upper[self.__height - 1 - lane][self.__width - 1] = 0
        return ret

    def __check_pull_top(self, lane):
        """
        :param lane: lane
        :return: if there is a space on intersection for new car from top, lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[0][self.__width - lane - 1]
        if isinstance(on_field, Car) and on_field.destination == Directions.TOP:
            return True
        return False

    def __check_pull_left(self, lane):
        """
        :param lane: lane
        :return: if there is a space on intersection for new car from left, lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[lane][0]
        if isinstance(on_field, Car) and on_field.destination == Directions.LEFT:
            return True
        return False

    def __check_pull_bottom(self, lane):
        """
        :param lane: lane
        :return: if there is a space on intersection for new car from bottom, lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[self.__height - 1][lane]
        if isinstance(on_field, Car) and on_field.destination == Directions.BOTTOM:
            return True
        return False

    def __check_pull_right(self, lane):
        """
        :param lane: lane
        :return: if there is a space on intersection for new car from right, lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[self.__height - 1 - lane][self.__width - 1]
        if isinstance(on_field, Car) and on_field.destination == Directions.RIGHT:
            return True
        return False

    @property
    def array(self):
        """
        :return:Array of cars on intersection
        """
        return self.__array_upper
