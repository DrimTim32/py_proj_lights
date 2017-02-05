"""This file contains Config class"""
import json


class Config:
    """
    Configuration class
    """
    def __init__(self, number_of_directions, directions, norm, variance, importance):
        self.number_of_directions = number_of_directions
        self.directions = directions
        self.norm = norm
        self.variance = variance
        self.importance = importance

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
        return Config(data['numberOfDirections'], data['directions'], data['norm'], data['variance'], data['importance'])

    @property
    def directions_lanes(self):
        """
        :return: returns crossroad topology
        :rtype: dict[int,tuple[int,int]]
        """
        return {direction.get('Id'): [direction.get('InLanes'), direction.get('OutLanes')] for direction in self.directions}

    @property
    def directions_turns(self):
        """
        :return: returns crossroad turns topology
        :rtype: dict[int,dict[int:dict[int:[float, bool]]]]
        """
        return {direction.get('Id'): {lane.get("LaneId"): {turn.get('Direction'): [turn.get('Probability'), turn.get('Safe')]  for turn in lane.get('TurnDirections')} for lane in direction.get('Lanes')} for direction in self.directions}