"""This file contains tests for car generator"""
import sys

from simulation import Directions, TurnDirection
from simulation.generators import CarProperGenerator

if "core" not in sys.path[0]:
    sys.path.insert(0, 'core')


def test_lights_generator():
    prob = {Directions.TOP: [[0, 0, 0]],
            Directions.BOTTOM: [[0, 0, 0], [1, 0, 0]],
            Directions.RIGHT: [[0, 1, 0]],
            Directions.LEFT: [[0, 0, 1]]}
    lg = CarProperGenerator(prob)
    assert lg.generate(Directions.TOP, 0) is None
    assert lg.generate(Directions.BOTTOM, 1).turn_direction == TurnDirection.RIGHT
    assert lg.generate(Directions.RIGHT, 0).turn_direction == TurnDirection.STRAIGHT
    assert lg.generate(Directions.LEFT, 0).turn_direction == TurnDirection.LEFT
