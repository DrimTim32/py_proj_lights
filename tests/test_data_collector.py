"""This file contains tests for data collector"""
import sys

from simulation import Directions, TurnDirection, Car, DataCollector
from simulation.data_collector import LanePhaseData

if "core" not in sys.path[0]:
    sys.path.insert(0, 'core')


def test_lanephase_data():
    lp = LanePhaseData(1)
    lp.car_count = 30
    lp.total_waiting_time = 330
    assert lp.average_waiting_time == 11


def test_data_collector():
    dc = DataCollector()
    car1 = Car(Directions.TOP, TurnDirection.LEFT)
    car1.waiting_time = 10
    car2 = Car(Directions.TOP, TurnDirection.LEFT)
    car2.waiting_time = 20
    car3 = Car(Directions.TOP, TurnDirection.LEFT)
    car3.waiting_time = 30
    car4 = Car(Directions.TOP, TurnDirection.LEFT)
    car4.waiting_time = 40
    car5 = Car(Directions.TOP, TurnDirection.LEFT)
    car5.waiting_time = 50
    dc.register(car1, 1, 0)
    dc.register(car2, 1, 0)
    dc.register(car3, 2, 1)
    dc.register(car4, 2, 1)
    dc.register(car5, 3, 1)
    assert dc.data[0][0].average_waiting_time == 15
    assert dc.data[1][0].average_waiting_time == 35
    assert dc.data[1][1].average_waiting_time == 50
