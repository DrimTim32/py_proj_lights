"""
File containing FixedLightsManagerClass
"""
from core.simulation.enums import Orientation


class FixedLightsManager:
    """
    FixedLightsManger class
    """

    def __init__(self, phases, lanes_info=None):
        """
        initializes LightsManager with lights phases and information about lanes on intersection
        :param phases: lights phases
        :param lanes_info: informations about lanes on intersection
        :type phases: list[LightsPhase]
        :type lanes_info: LanesData
        """
        self.current_phase = -1
        self.__previous_phase = -1
        self.__no_phase_time = 9
        self.__last_phase_change = 0
        self.__phases = phases
        self.__lanes_info = lanes_info

    def is_green(self, direction, lane_index):
        """
        :param direction: direction
        :param lane_index: lane index
        :return: if light is green on given lane in given direction
        :rtype: bool
        """

        phase = self.__phases[self.current_phase]
        lane = self.__lanes_info[direction.__str__()][lane_index]
        if self.current_phase == -1:
            return False
        if FixedLightsManager.__check_orientation(direction) == phase.orientation:
            return False
        if phase.right and lane.right:
            return True
        if phase.straight and lane.straight:
            return True
        if phase.left and lane.left:
            return True
        if phase.left_separated and lane.left_separated:
            return True
        return False

    def update(self):
        """
        updates lights
        :return: none
        """
        if self.current_phase == -1:
            if self.__last_phase_change == self.__no_phase_time:
                self.current_phase = (self.__previous_phase + 1) % len(self.__phases)
                self.__last_phase_change = 0
            else:
                self.__last_phase_change += 1
        else:
            if self.__last_phase_change == self.__phases[self.current_phase].duration:
                self.__previous_phase = self.current_phase
                self.current_phase = -1
                self.__last_phase_change = 0
            else:
                self.__last_phase_change += 1

    @staticmethod
    def __check_orientation(direction):
        return Orientation(direction % 2)
