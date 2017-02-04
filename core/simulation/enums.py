from enum import IntEnum


class Directions(IntEnum):
    TOP = 0
    LEFT = 1
    BOTTOM = 2
    RIGHT = 3

    def __str__(self):
        return self.name.lower()


class TurnDirection(IntEnum):
    RIGHT = 1
    STRAIGHT = 2
    LEFT = 3


class Orientation(IntEnum):
    VERTICAL = 0
    HORIZONTAL = 1


def str_to_direction(direction_str):
    if direction_str == "top":
        return Directions.TOP
    elif direction_str == "right":
        return Directions.RIGHT
    elif direction_str == "bottom":
        return Directions.BOTTOM
    elif direction_str == "left":
        return Directions.LEFT
