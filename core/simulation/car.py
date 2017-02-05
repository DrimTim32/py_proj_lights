"""This file contains Car class"""


class Car:
    """Car structure"""

    def __init__(self, source, turn_direction):
        """
        Initializes car from it's source and turn direction
        :param source: car's source
        :param turn_direction: car's source direction
        """
        self.__source = source
        self.__turn_direction = turn_direction
        self.__destination = (self.__source + self.__turn_direction) % 4
        self.waiting_time = 0

    @property
    def source(self):
        """
        :return: car's source direction
        :rtype: int
        """
        return self.__source

    @property
    def turn_direction(self):
        """
        :return: car's turn direction
        :rtype: TurnDirection
        """
        return self.__turn_direction

    @property
    def destination(self):
        """
        :return: car's destination direction of car
        :rtype: int
        """
        return self.__destination
