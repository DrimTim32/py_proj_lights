from core.simulation.car import Car


def test_car_init():
    c = Car(0, 0)
    assert c.source == 0
    assert c.turn_direction == 0
