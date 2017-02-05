from core.simulation.intersection import Intersection, IntersectionProperties
from core.simulation.road import RoadSizeVector
from core.data_structures.enums import Directions, TurnDirection
from core.simulation.car import Car


def test_one_car_update():
    road = [RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5)]
    properties = IntersectionProperties(road)
    intersection = Intersection(properties)
    intersection.push_car(Directions.TOP, 0, Car(0, TurnDirection.LEFT))
    for q in range(10):
        assert intersection[q][0] == 1
        intersection.update()
    assert intersection[9][0] != 1
    for q in range(8):
        assert intersection[9][q + 1] == 1
        intersection.update()
    print(intersection.array)

def test_few_car_update():
    road = [RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5)]
    properties = IntersectionProperties(road)
    intersection = Intersection(properties)
    intersection.push_car(Directions.TOP, 0, Car(0, TurnDirection.LEFT))
    intersection.push_car(Directions.TOP, 1, Car(0, TurnDirection.LEFT))
    intersection.push_car(Directions.TOP, 2, Car(0, TurnDirection.LEFT))
    intersection.push_car(Directions.TOP, 3, Car(0, TurnDirection.LEFT))
    intersection.push_car(Directions.TOP, 4, Car(0, TurnDirection.LEFT))
    for i in range(6):
        for q in range(5):
            assert intersection[i][q] == 1
        intersection.update()

    for q in range(4):
        assert intersection[6][q] == 1
