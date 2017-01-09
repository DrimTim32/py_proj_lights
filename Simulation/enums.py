from enum import IntEnum


class Directions(IntEnum):
    TOP = 0
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3


class TurnDirection(IntEnum):
    RIGHT = 1
    STRAIGHT = 2
    LEFT = 3
