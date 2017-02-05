"""
File containing CarProperGenerator class
"""
from numpy.random import choice

from core.data_structures.enums import TurnDirection
from core.simulation import Car


class CarProperGenerator:
    """
    CarProperGenerator class
    """

    def __init__(self, probability_info):
        """
        initializes generator with lanes info and probability info
        :param probability_info: probability info
        :type probability_info: dict[Directions,list[list[float]]]
        """
        self.__probability_info = probability_info

    def generate(self, direction, lane_index):
        """
        Generates car or none on given lane in gocen direction
        :param direction: direction
        :param lane_index:
        :type direction: Directions
        :type lane_index: int
        :return: generated Car or None
        :rtype: Car, None
        """
        probabilities = self.__probability_info[direction][lane_index]
        possibilities = [None,
                         Car(direction, TurnDirection.RIGHT),
                         Car(direction, TurnDirection.STRAIGHT),
                         Car(direction, TurnDirection.LEFT)]

        none_prob = 1. - sum(probabilities)
        ret = choice(possibilities, 1, p=[none_prob] + probabilities)
        if direction == 0:
            print([none_prob] + probabilities)
        return ret[0]
