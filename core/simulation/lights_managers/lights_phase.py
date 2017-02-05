"""
File containing LightsPhase class and supporting tools
"""
from collections import namedtuple

DirectionsInfo = namedtuple('DirectionsInfo', ['right', 'straight', 'left', 'left_separated'])


class LightsPhase:
    """
    LightsPhase class
    """

    def __init__(self, directions, orientation, duration):
        """
        initializes LightsPhase from its properties and duration time
        :param directions: phase properties
        :param orientation: orientation of driving during phase
        :param duration: duration time of phase
        :type directions: DirectionsInfo
        :type orientation: Orientation
        :type duration: int
        """
        self.__right = directions.right  # type : bool
        self.__straight = directions.straight  # type : bool
        self.__left = directions.left  # type : bool
        self.__left_separated = directions.left_separated  # type : bool
        self.__orientation = orientation  # type : Orientation
        self.__duration = duration  # type : int

    def __repr__(self):
        return str(self.right) + str(self.straight) + str(self.left) + str(self.left_separated) + str(self.orientation)

    def __eq__(self, other):
        return (self.__right == other.right or self.__straight == other.straight) and self.__left == other.left and \
               self.left_separated == other.left_separated and self.__orientation == other.orientation

    @property
    def right(self):
        """
        :return: if phase serves right turn
        :rtype: bool
        """
        return self.__right

    @property
    def straight(self):
        """
        :return: if phase serves going straight
        :rtype: bool
        """
        return self.__straight

    @property
    def left(self):
        """
        :return: if phase serves left turn
        :rtype: bool
        """
        return self.__left

    @property
    def left_separated(self):
        """
        :return: if phase serves separated left turn
        :rtype: bool
        """
        return self.__left_separated

    @property
    def orientation(self):
        """
        :return: orientation of driving during phase
        :rtype: Orientation
        """
        return self.__orientation

    @property
    def duration(self):
        """
        :return: phase duration
        :rtype: int
        """
        return self.__duration

    @duration.setter
    def duration(self, new_duration):
        """
        Sets new duration obtained by optimization
        :param new_duration: new duration
        :type new_duration: int
        :return: none
        """
        if new_duration < 0:
            raise ValueError("New duration should be non negative")
        self.__duration = new_duration
