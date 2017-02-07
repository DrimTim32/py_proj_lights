import sys
if "core" not in sys.path[0]:
    if "\\" in sys.path[0]:
        sys.path.insert(0, 'core')
    else:
        sys.path.insert(0, 'core')
from data_structures.enums import Directions, TurnDirection
from simulation.car import Car
from simulation.intersection import Intersection, IntersectionProperties
from simulation.road import RoadSizeVector


def get_intersection():
    road = [RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5), RoadSizeVector(10, 5, 5)]
    properties = IntersectionProperties(road)
    return Intersection(properties)


def test_one_top_left_update():
    intersection = get_intersection()
    intersection.push_car(Directions.TOP, 0, Car(Directions.TOP, TurnDirection.LEFT))
    for q in range(10):
        assert intersection[q][0] == 3
        intersection.update()
    assert intersection[9][0] != 1
    for q in range(8):
        assert intersection[9][q + 1] == 3
        intersection.update()


# region TOP DIRECTION
def test_multiple_top_left_update():
    intersection = get_intersection()
    for i in range(5):
        intersection.push_car(Directions.TOP, i, Car(Directions.TOP, TurnDirection.LEFT))
    for i in range(6):
        for q in range(5):
            assert intersection[i][q] == 3
        intersection.update()

    for q in range(4):
        assert intersection[6][q] == 3


def test_multiple_top_forward_update():
    intersection = get_intersection()
    for i in range(5):
        intersection.push_car(Directions.TOP, i, Car(Directions.TOP, TurnDirection.STRAIGHT))
    for i in range(9):
        for j in range(5):
            assert intersection[i][j] == 2
        intersection.update()
    for j in range(5):
        assert intersection[9][j] == 2


# endregion
# region RIGHT DIRECTION
def test_multiple_right_forward_update():
    intersection = get_intersection()
    for i in range(5):
        intersection.push_car(Directions.RIGHT, i, Car(Directions.RIGHT, TurnDirection.STRAIGHT))
    for i in range(9, 0, -1):
        for j in range(5):
            assert intersection[j][i] == 1
        intersection.update()

    for j in range(5):
        assert intersection[j][0] == 1


# endregion
# region LEFT DIRECTION
def test_multiple_left_forward_update():
    intersection = get_intersection()
    for i in range(5):
        intersection.push_car(Directions.LEFT, i, Car(Directions.LEFT, TurnDirection.STRAIGHT))
    for i in range(9):
        for j in range(5, 10):
            assert intersection[j][i] == 3
        intersection.update()

    for j in range(5, 10):
        assert intersection[j][9] == 3


def test_multiple_left_left_update():
    intersection = get_intersection()
    for i in range(5):
        intersection.push_car(Directions.LEFT, i, Car(Directions.LEFT, TurnDirection.LEFT))

    for i in range(6):
        for j in range(5, 10):
            assert intersection[j][i] != -1
        intersection.update()
    for _ in range(4):
        intersection.update()
    for i in range(5):
        assert intersection[2 * i][5 + i] != -1


# endregion

# region BOTTOM DIRECTION
def test_multiple_bottom_forward_update():
    intersection = get_intersection()
    for i in range(5):
        intersection.push_car(Directions.BOTTOM, i, Car(Directions.BOTTOM, TurnDirection.STRAIGHT))
    for i in range(9):
        for q in range(9, 4, -1):
            assert intersection[9 - i][q] == 0
        intersection.update()
    for q in range(9, 5, -1):
        assert intersection[0][q] == 0


def test_multiple_bottom_left_update():
    intersection = get_intersection()
    for i in range(5):
        intersection.push_car(Directions.BOTTOM, i, Car(Directions.BOTTOM, TurnDirection.LEFT))
    for i in range(9, 5, -1):
        for q in range(9, 5, -1):
            assert intersection[i][q] == 1
        intersection.update()
    for _ in range(5):
        intersection.update()
    for i in range(5):
        assert intersection[4 - i][2 * i + 1] == 1


# endregion


def test_pull_car():
    intersection = get_intersection()
    # top
    for i in range(5):
        intersection.push_car(Directions.TOP, 5 + i, Car(Directions.BOTTOM, TurnDirection.STRAIGHT))
    # bottom
    for i in range(5):
        intersection.push_car(Directions.BOTTOM, 5 + i, Car(Directions.TOP, TurnDirection.STRAIGHT))
    # left
    for i in range(5):
        intersection.push_car(Directions.LEFT, 5 + i, Car(Directions.RIGHT, TurnDirection.STRAIGHT))
    # right
    for i in range(5):
        intersection.push_car(Directions.RIGHT, 5 + i, Car(Directions.LEFT, TurnDirection.STRAIGHT))

    for i in range(5):
        assert intersection.pull_car(Directions.LEFT, i) is not None
        assert intersection.pull_car(Directions.LEFT, i) is None
        assert intersection.pull_car(Directions.TOP, i) is not None
        assert intersection.pull_car(Directions.TOP, i) is None

        assert intersection.pull_car(Directions.BOTTOM, i) is not None
        assert intersection.pull_car(Directions.BOTTOM, i) is None

        assert intersection.pull_car(Directions.RIGHT, i) is not None
        assert intersection.pull_car(Directions.RIGHT, 5 + i) is None
