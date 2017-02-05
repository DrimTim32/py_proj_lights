"""
File containing DataCollector class and supporting tools
"""


class LanePhaseData:
    def __init__(self, lane_identifier):
        self.car_count = 0
        self.lane_identifier = lane_identifier
        self.total_waiting_time = 0

    @property
    def average_waiting_time(self):
        return self.total_waiting_time / self.car_count

    def __repr__(self):
        return '|' + str(self.car_count) + " " + str(self.average_waiting_time) + '|'


class DataCollector:
    def __init__(self):
        """

        """
        self.data = {}  # dict[int, list[LanePhaseData]]

    def register(self, car, lane_index, current_phase):
        """
        registeres car data
        :param car: car
        :param lane_index: lane on which car was arriving intersection
        :param current_phase: current lights phase
        :type car: Car
        :type lane_index: int
        :type current_phase: int
        :return: none
        """
        lane_identifier = lane_index + car.source * 100
        if current_phase not in self.data.keys():
            self.data[current_phase] = []

        for phase_id in self.data.keys():
            if phase_id == current_phase:
                phase = self.data[phase_id]
                i = 0
                while i in range(len(phase)):
                    data = phase[i]
                    if data.lane_identifier == lane_identifier:
                        data.car_count += 1
                        data.total_waiting_time += car.waiting_time
                        break
                    i += 1
                if i == len(phase):
                    DataCollector._add_new_dataset(phase, lane_identifier, car)
                # print(phase)
                break

    @staticmethod
    def _add_new_dataset(phase, lane_identifier, car):
        data = LanePhaseData(lane_identifier)
        data.car_count = 1
        data.total_waiting_time = car.waiting_time
        phase.append(data)
