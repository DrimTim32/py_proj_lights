"""
File containing  LightsManager class
"""
from core.data_structures.enums import Orientation


class LightsManager:
    """
    LightsManger class
    """

    def __init__(self, phases, lanes_info):
        """
        initializes LightsManager with lights phases and information about lanes on intersection
        :param phases: lights phases
        :param lanes_info: information about lanes on intersection
        :type phases: list[LightsPhase]
        :type lanes_info: dict[Directions, list[DirectionsInfo]]
        """
        self.__current_phase = -1
        self.__previous_phase = -1
        self.__last_phase_change = 0
        self.__lanes_info = lanes_info
        self.__no_phase_time = 2 * max([len(dir_lanes) for dir_lanes in self.__lanes_info.values()])
        self.phases = phases

    def is_green(self, direction, lane_index):
        """
        :param direction: direction
        :param lane_index: lane index
        :type lane_index: int
        :type direction: Directions
        :return: if light is green on given lane in given direction
        :rtype: bool
        """
        phase = self.phases[self.current_phase]
        lane = self.__lanes_info[direction][lane_index]
        if self.__current_phase == -1:
            return False
        if LightsManager.__check_orientation(direction) != phase.orientation:
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
                self.__current_phase = (self.__previous_phase + 1) % len(self.phases)
                self.__last_phase_change = 0
            else:
                self.__last_phase_change += 1
        else:
            if self.__last_phase_change == self.phases[self.current_phase].duration:
                self.__previous_phase = self.current_phase
                self.__current_phase = -1
                self.__last_phase_change = 0
            else:
                self.__last_phase_change += 1

    @staticmethod
    def __check_orientation(direction):
        """
        :param direction: checks orientation of given direction
        :type direction: Direction
        :return: orientation
        :rtype: Orientation
        """
        return Orientation(direction % 2)

    @property
    def current_phase(self):
        """
        :return: cuurent phase
        :rtype: int
        """
        return self.__current_phase
