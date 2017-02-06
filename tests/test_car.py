import sys, os

from data_structures.enums import Directions, TurnDirection
from simulation.car import Car


def test_car_init():
    c = Car(Directions.TOP, TurnDirection.LEFT)
    assert c.source == Directions.TOP
    assert c.turn_direction == TurnDirection.LEFT
    assert c.waiting_time == 0
