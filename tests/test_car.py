import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
if "/" in sys.path[0]:
    sys.path.insert(0, myPath + '/../core')
else:
    sys.path.insert(0, myPath + '\\..\\core')

from data_structures.enums import Directions, TurnDirection
from simulation.car import Car


def test_car_init():
    c = Car(Directions.TOP, TurnDirection.LEFT)
    assert c.source == Directions.TOP
    assert c.turn_direction == TurnDirection.LEFT
    assert c.waiting_time == 0
