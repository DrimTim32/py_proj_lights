import pytest
import sys
import os
if "core" not in sys.path[0]:
    if "\\" in sys.path[0]:
        sys.path.insert(0, 'core')
    else:
        sys.path.insert(0, 'core')
from data_structures.enums import Directions, str_to_direction

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
