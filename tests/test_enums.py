import sys,os
myPath = os.path.dirname(os.path.abspath(__file__))
if "/" in sys.path[0]:
    sys.path.insert(0, myPath + '/../core')
else:
    sys.path.insert(0, myPath + '\\..\\core')

from data_structures.enums import Directions, str_to_direction
import pytest

data = [
    (Directions.TOP, "top"),
    (Directions.LEFT, "left"),
    (Directions.BOTTOM, "bottom"),
    (Directions.RIGHT, "right"),
]


@pytest.mark.parametrize("direction,expected", data)
def test_directions_to_string(direction, expected):
    assert str(direction) == expected


@pytest.mark.parametrize("direction,dir_string", data)
def test_str_to_dir(direction, dir_string):
    str_to_direction(dir_string) == direction


@pytest.mark.parametrize("dir_string", ["a", "asd", "213", "asd", "aa"])
def test_str_to_dir_exception(dir_string):
    with pytest.raises(ValueError) as excinfo:
        str_to_direction(dir_string)
    assert "direction" in str(excinfo.value).lower()
