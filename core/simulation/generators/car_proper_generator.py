import random

from core.simulation import Car
from core.simulation.enums import TurnDirection


class CarProperGenerator:
    def __init__(self, config=None):
        self.config = config

    def generate(self, direction, lane):
        right = [None, None, None, None,
                 Car(direction, TurnDirection.RIGHT)]
        right_n_straight = [None, None, None, None,
                            Car(direction, TurnDirection.RIGHT),
                            Car(direction, TurnDirection.STRAIGHT)]
        straight = [None, None, None, None,
                    Car(direction, TurnDirection.STRAIGHT)]
        left = [None, None, None, None,
                Car(direction, TurnDirection.LEFT)]
        if direction in {0, 2} and lane in {1}:
            return random.choice(straight)
        return None
