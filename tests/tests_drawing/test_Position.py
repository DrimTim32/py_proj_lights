import pytest

from DataStructures import Position


@pytest.mark.parametrize("a", (0, 10, 15))
@pytest.mark.parametrize("b", (0, 3, 5))
@pytest.mark.parametrize("c", (0, 7, 12))
@pytest.mark.parametrize("d", (0, 3, 9))
def test_sum(a, b, c, d):
    assert Position(a, b) + Position(c, d) == Position(a + c, b + d)


@pytest.mark.parametrize("a", (0, 1, 3))
@pytest.mark.parametrize("b", (0, 1, 5))
@pytest.mark.parametrize("c", (0, 1, 7))
@pytest.mark.parametrize("d", (0, 1, 8))
def test_substraction(a, b, c, d):
    assert Position(a, b) - Position(c, d) == Position(a - c, b - d)


@pytest.mark.parametrize("a", (0, 1, 2, 3, 4, 5))
@pytest.mark.parametrize("b", (0, 6, 7, 8, 11, 8))
def test_negation(a, b):
    assert -Position(a, b) == Position(-a, -b)

@pytest.mark.parametrize("a", (0, 1, 2, 3, 4, 5))
@pytest.mark.parametrize("b", (0, 6, 7, 8, 11, 8))
def test_copy(a, b):
    p1 = Position(a, b)
    p2 = p1.copy()
    assert not (p1 is p2)
    assert p1 == p2