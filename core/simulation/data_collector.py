"""
File containing DataCollector class and supporting tools
"""


class PhaseData:
    def __init__(self, lane_index):
        self.car_counr = 0
        self.lane_index = lane_index
        self.total_waiting_time = 0

    @property
    def average_waiting_time(self):
        return self.total_waiting_time / self.car_counr


class DataCollector:
    def __init__(self):
        """

        """
        self.__data = {}

    def register(self, car, lane_index, phase):
        """
        registeres car data
        :param car: car
        :param lane_index: lane on which car was arriving intersection
        :param phase: current lights phase
        :type car: Car
        :type lane_index: int
        :type phase: int
        :return: none
        """
        direction_data = car.destination.__str__()
        for phase in self.__data.keys():
            pass
