"""
File containing Config class
"""
import json


class Config:
    """
    Configuration class
    """

    def __init__(self, directions, roads_length, norm, variance, importance):
        self.__directions = directions
        self.__roads_length = roads_length
        self.__norm = norm
        self.__variance = variance
        self.__importance = importance

    @staticmethod
    def from_config_file(file_name):
        """
        :param file_name: name of file with configuration
        :type file_name: str
        :return: Config object constructed from given file
        :rtype: Config
        """
        file = open(file_name)
        data = json.load(file)
        return Config(data['directions'], data['roads_length'], data['norm'], data['variance'], data['importance'])

    @property
    def directions_lanes(self):
        """
        :return: returns crossroad topology
        :rtype: dict[int,tuple[int,int]]
        """
        return {direction.get('Id'): [direction.get('InLanes'), direction.get('OutLanes')] for direction in
                self.__directions}

    @property
    def directions_turns(self):
        """
        :return: returns crossroad turns topology
        :rtype: dict[int,list[dict[int,[float, bool]]]]
        """
        return {direction.get('Id'): [{turn.get('Direction'): [turn.get('Probability'), turn.get('Safe')] for turn in
                                       lane.get('TurnDirections')} for lane in direction.get('Lanes')] for direction in
                self.__directions}

    @property
    def roads_length(self):
        return self.__roads_length

    @property
    def norm(self):
        """
        :return: name of norm to be used in optimization
        :rtype: str
        """
        return self.__norm

    @property
    def variance(self):
        """
        :return: name of variance to be used in optimization
        :rtype: str
        """
        return self.__variance

    @property
    def importance(self):
        """
        :return: name of importance function
        :rtype: str
        """
        return self.__importance