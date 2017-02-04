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


road_len_parameters = [
    (Road([[], []]), 0),
    (Road([[], [[0]]]), 1),
    (Road([[[0]], [[0]]]), 1),
    (Road([[], [[0, 0]]]), 2),
    (Road([[], [[0, 0], [0, 0]]]), 2),
    (Road([[[0, 0], [0, 0]], [[0, 0], [0, 0]]]), 2),
    (Road([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0], [0, 0]]]), 3),
]


@pytest.mark.parametrize("road,expected_len", road_len_parameters)
def test_len(road, expected_len):
    assert road.length == expected_len


road_width_parameters = [
    (Road([[], []]), 0),
    (Road([[], [[0]]]), 1),
    (Road([[[0]], [[0]]]), 2),
    (Road([[], [[0, 0]]]), 1),
    (Road([[], [[0, 0], [0, 0]]]), 2),
    (Road([[[0, 0], [0, 0]], [[0, 0], [0, 0]]]), 4),
    (Road([[[0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0], [0, 0]]]), 5),
]


@pytest.mark.parametrize("road,expected_with", road_width_parameters)
def test_with(road, expected_with):
    assert road.width == expected_with


road_exceptions = [
    ([[], [[0, 0], [0]]], "In"),
    ([[], [[0, 0], [0, 0, 0]]], "In"),
    ([[[0, 0], [0, 0, 0]], []], "Out"),
    ([[[0, 0, 0], [0, 0], [0, 0, 0]], []], "Out"),
]


@pytest.mark.parametrize("road_data,str_contains", road_exceptions)
def test_raise_constructor_exception(road_data, str_contains):
    with pytest.raises(ValueError) as excinfo:
        Road(road_data)
    assert str_contains in str(excinfo.value)
