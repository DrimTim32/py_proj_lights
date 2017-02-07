"""
File containing Config class and SimulationData namedtuple
"""
import json
from collections import namedtuple

SimulationData = namedtuple('SimulationData', ['step_count',
                                               'simulation_count'])


class Config:
    """
    Configuration class
    """

    def __init__(self, directions, roads_length, simulation_data):
        """
        :type simulation_data : SimulationData
        """
        self.__directions = directions
        self.__roads_length = roads_length
        self.__simulation_data = SimulationData(int(simulation_data['step_count']),
                                                int(simulation_data['simulation_count']))

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
        return Config(data['directions'], data['roads_length'], data['simulation_data'])

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
        """Returns road lengths"""
        return self.__roads_length

    @property
    def simulation_data(self):
        """
        :return: name of norm to be used in optimization
        :rtype: SimulationData
        """
        return self.__simulation_data
