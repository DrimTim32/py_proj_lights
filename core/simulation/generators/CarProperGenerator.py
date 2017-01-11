import random

from core.simulation import Car
from core.simulation.enums import TurnDirection


class CarProperGenerator:
    def __init__(self, config=None):
        self.config = config

    def generate(self, direction, lane):
        right = [0, 0, 0, 0,
                 Car(direction, TurnDirection.RIGHT)]
        right_n_straight = [0, 0, 0, 0,
                            Car(direction, TurnDirection.RIGHT),
                            Car(direction, TurnDirection.STRAIGHT)]
        straight = [0, 0, 0, 0,
                    Car(direction, TurnDirection.STRAIGHT)]
        left = [0, 0, 0, 0,
                Car(direction, TurnDirection.LEFT)]
        if direction in {0, 1} and lane in {0, 1}:
            return random.choice(right)
        return 0
