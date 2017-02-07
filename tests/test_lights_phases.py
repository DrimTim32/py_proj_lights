"""This file contains tests for lights and phases"""
import sys

from simulation import DirectionsInfo, LightsPhase, Orientation, Directions
from simulation.lights_managers import LightsManager

if "core" not in sys.path[0]:
    sys.path.insert(0, 'core')


def test_lights_phase():
    phase1 = LightsPhase(DirectionsInfo(True, True, True, False), Orientation.VERTICAL, 20)
    phase2 = LightsPhase(DirectionsInfo(False, False, False, True), Orientation.VERTICAL, 20)
    phase3 = LightsPhase(DirectionsInfo(True, True, False, False), Orientation.VERTICAL, 20)

    assert phase1 == phase3
    assert not phase2 == phase3

    assert phase1.duration == 20
    assert phase1.left
    assert phase1.right
    assert phase1.straight
    assert not phase1.left_separated
    assert phase1.orientation == Orientation.VERTICAL

    phase1.duration = 30
    assert phase1.duration == 30
    phase3 += phase1
    assert phase3.right


def test_lights_manager():
    phase1 = LightsPhase(DirectionsInfo(True, True, True, False), Orientation.VERTICAL, 2)
    phase2 = LightsPhase(DirectionsInfo(False, False, False, True), Orientation.VERTICAL, 2)
    dire = {Directions.TOP: [1, 1],
            Directions.BOTTOM: [1, 1],
            Directions.RIGHT: [1, 1],
            Directions.LEFT: [1, 1]}
    lm = LightsManager([phase1, phase2], dire)
    assert not lm.is_green(0, 0)
    lm.update()
    lm.update()
    assert lm.current_phase == -1
    assert lm.in_phase_time == 2
    lm.update()
    lm.update()
    lm.update()
    assert lm.current_phase == 0
    assert lm.in_phase_time == 0
    lm.update()
    lm.update()
    lm.update()
    assert lm.current_phase == -1
    assert lm.in_phase_time == 0
