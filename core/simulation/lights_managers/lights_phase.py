"""
File containing LightsPhase namedtuple and supporting tools
"""
from collections import namedtuple

LightsPhaseDirections = namedtuple('LightsPhase', ['right', 'straight', 'left', 'left_separated'])


class LightsPhase:
    """
    LightsPhase class
    """

    def __init__(self, directions, duration):
        """
        initializes LightsPhase from its properties and duration time
        :param directions: phase properties
        :param duration: duration time of phase
        :type directions: LightsPhaseDirections
        :type duration: int
        """
        self.__right = directions.right  # type : bool
        self.__straight = directions.straight  # type : bool
        self.__left = directions.left  # type : bool
        self.__left_separated = directions.ledt_separated  # type : bool
        self.__duration = duration  # type : int

    @property
    def right(self):
        return self.__right

    @property
    def straight(self):
        return self.__straight

    @property
    def left(self):
        return self.left

    @property
    def left_separated(self):
        return self.left_separated

    @property
    def duration(self):
        return self.duration

    @duration.setter
    def duration(self, new_duration):
        self.__duration = new_duration
