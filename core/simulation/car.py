"""This file contains Car class"""


class Car:
    """Car structure"""

    def __init__(self, source, turn_direction):
        self.__source = source
        self.__turn_direction = turn_direction
        self.__destination = (self.source + self.turn_direction) % 4
        self.waiting_time = 0

    @property
    def source(self):
        return self.__source

    @property
    def turn_direction(self):
        return self.__turn_direction

    @property
    def destination(self):
        return self.__destination
