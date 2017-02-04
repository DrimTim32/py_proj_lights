"""
File containing Intersection class and supporting tools
"""

import numpy as np

from core.simulation.car import Car
from core.simulation.enums import Directions, TurnDirection, Orientation


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
        self.__array_upper = [[None for _ in range(properties.width)] for _ in range(properties.height)]
        self.__array_lower = [[None for _ in range(properties.width)] for _ in range(properties.height)]
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
        self.__update_right_part_left()
        self.__update_right_part_right()

    def __update_right_part_left(self):
        """
        updates positions of cars turning right on the left part of the intersection
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
                    self.__array_upper[row][col] = None

        # bottom left quarter
        for col in range(self.__properties.bottom.out_lanes_count - 1, -1, -1):
            for row in range(self.__height - 1, self.__height - 1 - self.__properties.left.in_lanes_count, -1):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.__height - row > self.__properties.bottom.out_lanes_count - col:
                        self.__array_upper[row + 1][col] = on_field
                    else:
                        self.__array_upper[row][col + 1] = on_field
                    self.__array_upper[row][col] = None

    def __update_right_part_right(self):
        """
        updates positions of cars turning right on the right part of the intersection
        :return: none
        """
        # bottom right quarter
        for row in range(self.__height - self.__properties.right.out_lanes_count, self.__height):
            for col in range(self.__width - 1, self.__width - 1 - self.__properties.bottom.in_lanes_count, -1):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.__height - row < self.__width - col:
                        self.__array_upper[row - 1][col] = on_field
                    else:
                        self.__array_upper[row][col + 1] = on_field
                    self.__array_upper[row][col] = None

        # top right quarter
        for col in range(self.__width - self.__properties.bottom.out_lanes_count, self.__width):
            for row in range(self.__properties.right.in_lanes_count):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.RIGHT:
                    if self.__properties.right.in_lanes_count - row < self.__width - col:
                        self.__array_upper[row - 1][col] = on_field
                    else:
                        self.__array_upper[row][col - 1] = on_field
                    self.__array_upper[row][col] = None

    def __update_straight(self):
        """
        updates positions of cars going straight
        :return: none
        """
        orientation = self.__check_orientation()
        if orientation is None:
            return
        if orientation == Orientation.VERTICAL:
            self.__update_straight_vertical()
        else:
            self.__update_straight_horizontal()

    def __update_straight_vertical(self):
        """
        updates positions of cars going straight on vertical light phase
        :return: none
        """
        # left half
        for row in range(self.__height - 1, -1, - 1):
            for col in range(self.__properties.top.in_lanes_count):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    print(row, col)
                    self.__array_upper[row + 1][col] = on_field
                    self.__array_upper[row][col] = None

        # right half
        for row in range(self.__height):
            for col in range(self.__width - self.__properties.bottom.in_lanes_count, self.__width):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    self.__array_upper[row - 1][col] = on_field
                    self.__array_upper[row][col] = None

    def __update_straight_horizontal(self):
        """
        updates positions of cars going straight on horizontal light phase
        :return: none
        """
        # top half
        for col in range(self.__width):
            for row in range(self.__properties.right.in_lanes_count):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    self.__array_upper[row][col - 1] = on_field
                    self.__array_upper[row][col] = None

        # bottom half
        for col in range(self.__width - 1, -1, -1):
            for row in range(self.__height - self.__properties.left.in_lanes_count, self.__height):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field, Car) and on_field.turn_direction == TurnDirection.STRAIGHT:
                    self.__array_upper[row][col + 1] = on_field
                    self.__array_upper[row][col] = None

    def __update_left(self):
        """
        updates positions of cars turning left
        :return: none
        """
        orientation = self.__check_orientation()
        if orientation is None:
            return
        if orientation == Orientation.VERTICAL:
            self.__update_left_vertical()
        else:
            self.__update_left_horizontal()

    def __update_left_horizontal(self):
        """
        updates positions of cars turning left on  horizontal light phase
        :return: none
        """
        for col in range(self.__width):
            for row in range(self.__height - 1, -1, -1):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field,
                              Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 3:
                    in_lane_base = self.__properties.right.in_lanes_count - row
                    if col > self.__width - self.__properties.bottom.in_lanes_count - in_lane_base:
                        self.__array_upper[row][col - 1] = on_field
                    else:
                        self.__array_upper[row + 1][col] = on_field
                    self.__array_upper[row][col] = None

        for col in range(self.__width - 1, -1, -1):
            for row in range(self.__height):
                on_field = self.__array_lower[row][col]
                if isinstance(on_field,
                              Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 1:
                    in_lane_base = self.__height - self.__properties.left.out_lanes_count - row
                    if col < self.__width - self.__properties.top.out_lanes_count - in_lane_base:
                        self.__array_lower[row][col + 1] = on_field
                    else:
                        self.__array_lower[row - 1][col] = on_field
                    self.__array_lower[row][col] = None

    def __update_left_vertical(self):
        """
        updates positions of cars turning left on  vertical light phase
        :return: none
        """
        for row in range(self.__height - 1, -1, -1):
            for col in range(self.__width - 1, -1, -1):
                on_field = self.__array_upper[row][col]
                if isinstance(on_field,
                              Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 0:
                    in_lane_base = self.__properties.top.in_lanes_count - col - 1
                    if row < self.__height - self.__properties.right.out_lanes_count + in_lane_base:
                        self.__array_upper[row + 1][col] = on_field
                    else:
                        self.__array_upper[row][col + 1] = on_field
                    self.__array_upper[row][col] = None

        for row in range(self.__height):
            for col in range(self.__width):
                on_field = self.__array_lower[row][col]
                if isinstance(on_field,
                              Car) and on_field.turn_direction == TurnDirection.LEFT and on_field.source == 2:
                    in_lane_base = self.__width - self.__properties.bottom.out_lanes_count - col
                    if row >= self.__height - self.__properties.left.out_lanes_count + in_lane_base:
                        self.__array_lower[row - 1][col] = on_field
                    else:
                        self.__array_lower[row][col - 1] = on_field
                    self.__array_lower[row][col] = None

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
        for row in self.__array_lower:
            for cell in row:
                if isinstance(cell, Car):
                    return cell.source % 2
        return None

    def push_car(self, direction, lane_index, car):
        """
        Adds car from road to the intersection
        :param direction: direction from which car is arriving
        :param lane_index: lane from which car is ariving
        :param car: Car
        :type direction: Directions
        :type lane_index: int
        :type car: Car
        :return: none
        """
        if direction == Directions.TOP:
            self.__array_upper[0][lane_index] = car
        elif direction == Directions.LEFT:
            if car.turn_direction == TurnDirection.LEFT:
                self.__array_lower[self.__height - 1 - lane_index][0] = car
            else:
                self.__array_upper[self.__height - 1 - lane_index][0] = car
        elif direction == Directions.BOTTOM:
            if car.turn_direction == TurnDirection.LEFT:
                self.__array_lower[self.__height - 1][self.__width - lane_index - 1] = car
            else:
                self.__array_upper[self.__height - 1][self.__width - lane_index - 1] = car
        else:  # RIGHT
            self.__array_upper[lane_index][self.__width - 1] = car

    def pull_car(self, direction, lane_index, offset=0):
        """
        Removes car from intersection and returns it
        :param direction: direction in which car is going
        :param lane_index: lane in which car is going
        :param offset: offset between lanes on intersection and lanes on road
        :type direction: Directions
        :type lane_index: int
        :type offset: int
        :return: car
        :rtype: Car
        """
        ret = None
        if direction == Directions.TOP and self.__check_pull_upper_top(lane_index):
            ret = self.__array_upper[0][self.__width - lane_index - 1]
            self.__array_upper[0][self.__width - lane_index - 1] = None
        elif direction == Directions.TOP and self.__check_pull_lower_top(lane_index):
            ret = self.__array_lower[0][self.__width - lane_index - 1]
            self.__array_lower[0][self.__width - lane_index - 1] = None

        elif direction == Directions.LEFT and self.__check_pull_upper_left(lane_index):
            ret = self.__array_upper[lane_index][0]
            self.__array_upper[lane_index][0] = None
        elif direction == Directions.LEFT and self.__check_pull_lower_left(lane_index):
            ret = self.__array_lower[lane_index][0]
            self.__array_lower[lane_index][0] = None

        elif direction == Directions.BOTTOM and self.__check_pull_bottom(lane_index):
            ret = self.__array_upper[self.__height - 1][lane_index]
            self.__array_upper[self.__height - 1][lane_index] = None

        elif direction == Directions.RIGHT and self.__check_pull_right(lane_index):
            ret = self.__array_upper[self.__height - 1 - lane_index][self.__width - 1]
            self.__array_upper[self.__height - 1 - lane_index][self.__width - 1] = None

        return ret

    def __check_pull_upper_top(self, lane_index):
        """
        :param lane_index: lane
        :type lane_index: int
        :return: if there is a car on intersection going to direction top from upper array on lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[0][self.__width - lane_index - 1]
        if isinstance(on_field, Car) and on_field.destination == Directions.TOP:
            return True
        return False

    def __check_pull_lower_top(self, lane_index):
        """
        :param lane_index: lane
        :type lane_index: int
        :return: if there is a car on intersection going to direction top from lower array on lane number lane
        :rtype: bool
        """
        on_field = self.__array_lower[0][self.__width - lane_index - 1]
        if isinstance(on_field, Car) and on_field.destination == Directions.TOP:
            return True
        return False

    def __check_pull_upper_left(self, lane_index):
        """
        :param lane_index: lane
        :type lane_index: int
        :return:  if there is a car on intersection going to direction left from upper array on lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[lane_index][0]
        if isinstance(on_field, Car) and on_field.destination == Directions.LEFT:
            return True
        return False

    def __check_pull_lower_left(self, lane_index):
        """
        :param lane_index: lane
        :type lane_index: int
        :return: if there is a car on intersection going to direction left from lower array on lane number lane
        :rtype: bool
        """
        on_field = self.__array_lower[lane_index][0]
        if isinstance(on_field, Car) and on_field.destination == Directions.LEFT:
            return True
        return False

    def __check_pull_bottom(self, lane_index):
        """
        :param lane_index: lane
        :type lane_index: int
        :return: if there is a car on intersection going to direction bottom on lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[self.__height - 1][lane_index]
        if isinstance(on_field, Car) and on_field.destination == Directions.BOTTOM:
            return True
        return False

    def __check_pull_right(self, lane_index):
        """
        :param lane_index: lane
        :type lane_index: int
        :return: if there is a car on intersection going to direction right on lane number lane
        :rtype: bool
        """
        on_field = self.__array_upper[self.__height - 1 - lane_index][self.__width - 1]
        if isinstance(on_field, Car) and on_field.destination == Directions.RIGHT:
            return True
        return False

    @property
    def array(self):
        """
        :return:Array of cars on intersection
        """
        out_array = np.empty(np.array(self.__array_upper).shape)
        for i in range(len(self.__array_upper)):
            for j in range(len(self.__array_upper[i])):
                out_array[i][j] = (self.__array_upper[i][j] is not None) or (self.__array_lower[i][j] is not None)
        return out_array.astype(int)
