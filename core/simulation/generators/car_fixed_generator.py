import random

from core.data_structures.enums import TurnDirection
from core.simulation import Car


class CarFixedGenerator:
    def __init__(self, lanes_info):
        self.__lanes_info = lanes_info

    def generate(self, direction, lane_index):
        right = [None, None, None, None,
                 Car(direction, TurnDirection.RIGHT)]
        right_n_straight = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                            None, None, None, None, None, None, None,
                            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                            None, None, None, None, None, None, None,
                            Car(direction, TurnDirection.RIGHT),
                            Car(direction, TurnDirection.STRAIGHT)]
        straight = [None, None, None, None,
                    Car(direction, TurnDirection.STRAIGHT)]
        left = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None,
                Car(direction, TurnDirection.LEFT)]

        if lane_index in {0}:
            return random.choice(right_n_straight)
        if lane_index in {1}:
            return random.choice(left)
        return None
