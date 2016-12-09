from Drawing.DataStructures.Position import Position
import pytest

data = [
    (Position(1, 1), Position(1, 1), Position(2,2)),
    (Position(2, 2), Position(2, 2), Position(4,4)),
    (Position(3, 7), Position(3, 7), Position(6,14)),
    (Position(7, 3), Position(7, 3), Position(14,6)),

]


@pytest.mark.parametrize("a,b,expected", data)
def test_sum(a, b, expected):
    assert (a + b) == expected
