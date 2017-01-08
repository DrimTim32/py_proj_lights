import random


class CarRandomGenerator:
    def __init__(self):
        pass

    def generate(self, direction, lane):
        return random.choice([0, 0, 0, 0, 0, 1]) if direction == 0 else 0
