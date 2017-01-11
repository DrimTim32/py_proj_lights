import random

from core.simulation import Car
from core.simulation.enums import TurnDirection


class CarProperGenerator:
    def __init__(self):
        pass

    def generate(self, direction, lane):
        return random.choice([0, 0, 0, 0, Car(direction, TurnDirection.RIGHT)]) if direction == 0 else 0
