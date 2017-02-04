class FixedLightsManager:
    def __init__(self, phases):
        self.__current_phase = -1
        self.__no_phase_time = 10
        self.__last_phase_change = 0
        self.__phases = phases

    def is_green(self, direction, lane):
        return True

    def update(self):
        pass
