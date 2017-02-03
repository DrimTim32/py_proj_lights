import pytest

from core.data_structures.road import get_empty_road, RoadSizeVector, Road

empty_roads_data = [
    (RoadSizeVector(1, 1, 0), [[[0]], []]),
    (RoadSizeVector(1, 1, 1), [[[0]], [[0]]]),
    (RoadSizeVector(2, 1, 1), [[[0, 0]], [[0, 0]]]),
    (RoadSizeVector(2, 2, 1), [[[0, 0], [0, 0]], [[0, 0]]]),
    (RoadSizeVector(2, 2, 2), [[[0, 0], [0, 0]], [[0, 0], [0, 0]]]),
    (RoadSizeVector(2, 1, 2), [[[0, 0]], [[0, 0], [0, 0]]]),
    (RoadSizeVector(7, 3, 2), [
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
    ]),
]

yield_first_data = [
    (Road([[], []]), []),
    (Road([[[0]], []]), [(0, 0)]),
    (Road([[[0]], [[0]]]), [(0, 0)]),
    (Road([[[0, 0]], []]), [(0, 0), (0, 1)]),
    (Road([[[0, 0], [0, 0]], []]), [(0, 0), (0, 1), (1, 0), (1, 1)]),
]
yield_second_data = [
    (Road([[], []]), []),
    (Road([[], [[0]]]), [(0, 0)]),
    (Road([[[0]], [[0]]]), [(0, 0)]),
    (Road([[], [[0, 0]]]), [(0, 0), (0, 1)]),
    (Road([[], [[0, 0], [0, 0]]]), [(0, 0), (0, 1), (1, 0), (1, 1)]),
]


@pytest.mark.parametrize("vector,expected", empty_roads_data)
def test_generate_empty_road(vector, expected):
    assert get_empty_road(vector).out_lanes == expected[0]
    assert get_empty_road(vector).in_lanes == expected[1]


@pytest.mark.parametrize("vector,expected", yield_first_data)
def test_yielding_first_indexes(vector, expected):
    i = 0
    output = [(x, y) for (x, y) in vector.out_indexes]
    assert len(output) == len(expected), "{0}".format(expected)
    assert output == expected


@pytest.mark.parametrize("vector,expected", yield_second_data)
def test_yielding_second_indexes(vector, expected):
    i = 0
    output = [(x, y) for (x, y) in vector.in_indexes]
    assert len(output) == len(expected), "{0}".format(expected)
    assert output == expected
