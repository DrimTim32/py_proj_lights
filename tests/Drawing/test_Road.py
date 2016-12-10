from Drawing.DataStructures.Road import get_empty_road, RoadSizeVector
import pytest

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


@pytest.mark.parametrize("vector,expected", empty_roads_data)
def test_generate_empty_road(vector, expected):
    assert get_empty_road(vector).first == expected[0]
    assert get_empty_road(vector).second == expected[1]
