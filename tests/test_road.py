import numpy as np
import pytest

from data_structures.enums import Directions, TurnDirection
from simulation.car import Car
from simulation.road import get_empty_road, RoadSizeVector, Road

empty_roads_data = [
    (RoadSizeVector(1, 1, 1), [[[None]], [[None]]]),
    (RoadSizeVector(2, 1, 1), [[[None, None]], [[None, None]]]),
    (RoadSizeVector(2, 2, 2), [[[None, None], [None, None]], [[None, None], [None, None]]]),
    (RoadSizeVector(7, 3, 3), [
        [
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None]
        ],
        [
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None]
        ]
    ]),
]


@pytest.mark.parametrize("vector,expected", empty_roads_data)
def test_generate_empty_road(vector, expected):
    assert get_empty_road(vector).out_lanes == expected[0]
    assert get_empty_road(vector).in_lanes == expected[1]


yield_first_data = [
    (Road([[], []]), []),
    (Road([[[0]], [[0]]]), [(0, 0)]),
    (Road([[[0, 0]], [[0, 0]]]), [(0, 0), (0, 1)]),
]


@pytest.mark.parametrize("vector,expected", yield_first_data)
def test_yielding_first_indexes(vector, expected):
    output = [(x, y) for (x, y) in vector.out_indexes]
    assert len(output) == len(expected), "{0}".format(expected)
    assert output == expected


yield_second_data = [
    (Road([[], []]), []),
    (Road([[[0]], [[0]]]), [(0, 0)]),
    (Road([[[0, 0], [0, 0]], [[0, 0], [0, 0]]]), [(0, 0), (0, 1), (1, 0), (1, 1)]),
]


@pytest.mark.parametrize("vector,expected", yield_second_data)
def test_yielding_second_indexes(vector, expected):
    output = [(x, y) for (x, y) in vector.in_indexes]
    assert len(output) == len(expected)
    assert output == expected


road_len_parameters = [
    (Road([[], []]), 0),
    (Road([[[0]], [[0]]]), 1),
    (Road([[[0, 0], [0, 0]], [[0, 0], [0, 0]]]), 2),
    (Road([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]), 3),
]


@pytest.mark.parametrize("road,expected_len", road_len_parameters)
def test_len(road, expected_len):
    assert road.length == expected_len


road_width_parameters = [
    (Road([[], []]), 0),
    (Road([[[0]], [[0]]]), 2),
    (Road([[[0, 0], [0, 0]], [[0, 0], [0, 0]]]), 4),
    (Road([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]), 6),
]


@pytest.mark.parametrize("road,expected_with", road_width_parameters)
def test_with(road, expected_with):
    assert road.width == expected_with


road_exceptions = [
    ([[], [[0, 0], [0]]], "in"),
    ([[], [[0, 0], [0, 0, 0]]], "in"),
    ([[[0, 0], [0, 0, 0]], []], "out"),
    ([[[0, 0, 0], [0, 0], [0, 0, 0]], []], "out"),
]


@pytest.mark.parametrize("road_data,str_contains", road_exceptions)
def test_raise_constructor_exception(road_data, str_contains):
    with pytest.raises(ValueError) as excinfo:
        Road(road_data)
    assert str_contains in str(excinfo.value).lower()


@pytest.mark.parametrize("road,expected_in_width,expected_out_width", [
    (Road([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]), 3, 3),
    (Road([[[0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0]]]), 2, 2),
    (Road([[[0, 0]], [[0, 0]]]), 1, 1),
])
def test_road_width(road, expected_in_width, expected_out_width):
    assert road.out_width == expected_out_width
    assert road.in_width == expected_in_width


def test_car_pull_push_out():
    road = Road([[[None, None, None], [None, None, None], [None, None, None]],
                 [[None, None, None], [None, None, None], [None, None, None]]])
    road.push_car_out(0, Car(Directions.BOTTOM, TurnDirection.LEFT))
    arr = np.array(road.out_lanes)
    assert len(arr[arr != np.array(None)]) == 1
    assert arr[0][0] is not None and isinstance(arr[0][0], Car)
    for _ in range(10):
        road.push_car_out(0, Car(Directions.BOTTOM, TurnDirection.LEFT))

    arr = np.array(road.out_lanes)
    assert len(arr[arr != np.array(None)]) == 1
    assert arr[0][0] is not None and isinstance(arr[0][0], Car)
    road.push_car_out(1, Car(Directions.BOTTOM, TurnDirection.LEFT))
    arr = np.array(road.out_lanes)
    assert len(arr[arr != np.array(None)]) == 2
    assert arr[0][0] is not None and isinstance(arr[0][0], Car) and arr[1][0] is not None and isinstance(arr[1][0], Car)


def test_car_pull_push_in():
    road = Road([[[None, None, None], [None, None, None], [None, None, None]],
                 [[None, None, None], [None, None, None], [None, None, None]]])
    road.push_car_in(0, Car(Directions.BOTTOM, TurnDirection.LEFT))
    arr = np.array(road.in_lanes)
    assert len(arr[arr != np.array(None)]) == 1
    assert arr[0][0] is not None and isinstance(arr[0][0], Car)
    for _ in range(10):
        road.push_car_in(0, Car(Directions.BOTTOM, TurnDirection.LEFT))

    arr = np.array(road.in_lanes)
    assert len(arr[arr != np.array(None)]) == 1
    assert arr[0][0] is not None and isinstance(arr[0][0], Car)
    road.push_car_in(1, Car(Directions.BOTTOM, TurnDirection.LEFT))
    arr = np.array(road.in_lanes)
    assert len(arr[arr != np.array(None)]) == 2
    assert arr[0][0] is not None and isinstance(arr[0][0], Car) and arr[1][0] is not None and isinstance(arr[1][0], Car)


def test_update_in_not_at_end():
    road = Road([
        [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ],
        [
            [Car(Directions.BOTTOM, TurnDirection.LEFT), None, None],
            [None, None, None],
            [Car(Directions.BOTTOM, TurnDirection.LEFT), None, None]
        ]
    ])
    road.update_in(0)
    assert road.in_lanes[0][0] is None and road.in_lanes[0][1] is not None and isinstance(road.in_lanes[0][1], Car)
    road.update_in(1)
    assert road.in_lanes[1][0] is None and road.in_lanes[1][1] is None
    road.update_in(2)
    assert road.in_lanes[2][0] is None and road.in_lanes[2][1] is not None and isinstance(road.in_lanes[2][1], Car)


def test_update_in_middle():
    road = Road([
        [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ],
        [
            [None, Car(Directions.BOTTOM, TurnDirection.LEFT), None],
            [None, None, None],
            [None, Car(Directions.BOTTOM, TurnDirection.LEFT), None]
        ]
    ])
    road.update_in(0)
    road.update_in(1)
    road.update_in(2)
    assert road.in_lanes[0][1] is None
    assert road.in_lanes[0][2] is not None
    assert isinstance(road.in_lanes[0][2], Car)
    assert road.in_lanes[1][1] is None
    assert road.in_lanes[1][2] is None
    assert road.in_lanes[2][1] is None
    assert road.in_lanes[2][2] is not None
    assert isinstance(road.in_lanes[2][2], Car)


def test_update_in_two():
    road = Road([
        [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ],
        [
            [Car(Directions.BOTTOM, TurnDirection.LEFT), Car(Directions.BOTTOM, TurnDirection.LEFT), None],
            [None, None, None],
            [Car(Directions.BOTTOM, TurnDirection.LEFT), Car(Directions.BOTTOM, TurnDirection.LEFT), None]
        ]
    ])
    road.update_in(0)
    assert road.in_lanes[0][1] is not None
    assert isinstance(road.in_lanes[0][1], Car)
    assert road.in_lanes[0][2] is not None
    assert isinstance(road.in_lanes[0][2], Car)
    road.update_in(1)
    assert road.in_lanes[1][1] is None
    assert road.in_lanes[1][2] is None
    road.update_in(2)
    assert road.in_lanes[2][1] is not None
    assert isinstance(road.in_lanes[2][1], Car)
    assert road.in_lanes[2][2] is not None
    assert isinstance(road.in_lanes[2][2], Car)


def test_update_in_at_end():
    road = Road([
        [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ],
        [
            [None, None, Car(Directions.BOTTOM, TurnDirection.LEFT)],
            [None, None, None],
            [None, None, Car(Directions.BOTTOM, TurnDirection.LEFT)]
        ]
    ])
    road.update_in(0)
    assert road.in_lanes[0][2] is not None
    assert isinstance(road.in_lanes[0][2], Car)
    assert road.in_lanes[0][2].waiting_time == 1
    road.update_in(1)
    assert road.in_lanes[1][2] is None
    road.update_in(2)
    assert road.in_lanes[2][2] is not None
    assert isinstance(road.in_lanes[2][2], Car)
    assert road.in_lanes[2][2].waiting_time == 1
    for _ in range(4):
        road.update_in(0)
        road.update_in(2)

    assert road.in_lanes[0][2].waiting_time == 5
    assert road.in_lanes[2][2].waiting_time == 5


def test_update_out_at_end():
    road = Road([
        [
            [None, None, Car(Directions.BOTTOM, TurnDirection.LEFT)],
            [None, None, None],
            [None, None, Car(Directions.BOTTOM, TurnDirection.LEFT)]
        ],
        [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    ])
    road.update_out()
    assert road.out_lanes[0][2] is None
    assert road.out_lanes[1][2] is None
    assert road.out_lanes[2][2] is None


def test_update_out_middle():
    road = Road([
        [
            [None, Car(Directions.BOTTOM, TurnDirection.LEFT), None],
            [None, None, None],
            [None, Car(Directions.BOTTOM, TurnDirection.LEFT), None]
        ],
        [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    ])
    road.update_out()
    assert road.out_lanes[0][2] is not None
    assert isinstance(road.out_lanes[0][2], Car)
    assert road.out_lanes[1][2] is None
    assert road.out_lanes[2][2] is not None
    assert isinstance(road.out_lanes[2][2], Car)


def test_update_out_three():
    road = Road([
        [
            [Car(Directions.BOTTOM, TurnDirection.LEFT), Car(Directions.TOP, TurnDirection.LEFT),
             Car(Directions.BOTTOM, TurnDirection.LEFT)],
            [None, None, None],
            [None, None, None]
        ],
        [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    ])
    road.update_out()
    assert road.out_lanes[0][0] is None
    assert road.out_lanes[0][1] is not None
    assert isinstance(road.out_lanes[0][1], Car)
    assert road.out_lanes[0][1].source == Directions.BOTTOM
    assert road.out_lanes[0][2] is not None
    assert isinstance(road.out_lanes[0][2], Car)
    assert road.out_lanes[0][2].source == Directions.TOP


def test_pull_no_car():
    road = Road([
        [
            [None, None, None],
            [None, None, None],
        ],
        [
            [Car(Directions.BOTTOM, TurnDirection.LEFT), Car(Directions.BOTTOM, TurnDirection.LEFT), None],
            [Car(Directions.BOTTOM, TurnDirection.LEFT), Car(Directions.BOTTOM, TurnDirection.LEFT), None],
        ]
    ])
    assert road.pull_car(0) is None
    assert road.pull_car(1) is None


def test_pull_car():
    road = Road([
        [
            [None, None, None],
            [None, None, None],
        ],
        [
            [None, None, Car(Directions.BOTTOM, TurnDirection.LEFT)],
            [None, None, Car(Directions.TOP, TurnDirection.LEFT)],
        ]
    ])
    car1 = road.pull_car(1)
    car0 = road.pull_car(0)
    assert car0 is not None
    assert isinstance(car0, Car)
    assert car0.source == Directions.BOTTOM
    assert car1 is not None
    assert isinstance(car1, Car)
    assert car1.source == Directions.TOP


def test_waiting_car():
    road = Road([
        [
            [None, None, None],
            [None, None, None],
        ],
        [
            [None, None, Car(Directions.TOP, TurnDirection.LEFT)],
            [None, None, None],
        ]
    ])
    assert road.has_waiting_car(0)
    assert not road.has_waiting_car(1)
