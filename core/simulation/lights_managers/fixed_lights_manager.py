"""
File containing FixedLightsManagerClass
"""


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
        self.__no_phase_time = 15
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
        if self.current_phase == -1:
            return False
        return True

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
