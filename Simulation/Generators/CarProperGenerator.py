import random

from Simulation import Car
from Simulation.enums import TurnDirection


class CarRandomGenerator:
    def __init__(self):
        pass

    def generate(self, direction, lane):
        return random.choice([0, 0, 0, 0, Car(direction, TurnDirection.RIGHT)]) if direction >= 0 else 0
