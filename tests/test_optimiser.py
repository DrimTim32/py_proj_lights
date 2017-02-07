"""This file contains tests for optimiser and connected algorithms"""

import pytest
import sys

if "core" not in sys.path[0]:
    sys.path.insert(0, 'core')
from algorithms.algorithms import get_norm, logistic, negative_gompertz

from configuration.config import Config, SimulationData


def test_norms():
    """This function tests norms """
    test1 = get_norm('euclid')
    test2 = get_norm('inf')
    test3 = get_norm('-inf')
    vector = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert pytest.approx(test1(vector)) == 19.6214
    assert pytest.approx(test2(vector)) == 10
    assert pytest.approx(test3(vector)) == 1


def test_bad_norms():
    for q in ["ads", "asd", 'ssad', 'a']:
        with pytest.raises(ValueError) as excinfo:
            get_norm(q)
        assert "any known" in str(excinfo.value).lower()


def test_logistic():
    """This function tests logistic curves, manual calculations done in mathematica"""
    assert pytest.approx(logistic(5.0, 2.0, 15.0, 500.0), 0.00001) == 0.99
    assert pytest.approx(logistic(2.0, 5.0, 15.0, 500.0), 0.00001) == 2.4675


def test_negative_gompertz():
    """This function tests negative gompertz curves, manual calculations done in mathematica"""
    assert pytest.approx(negative_gompertz(1, 1.0, 5.0, 5.0 / 1000), 0.00001) == 0.993092
    assert pytest.approx(negative_gompertz(600, 1.0, 5.0, 5.0 / 1000), 0.00001) == 0.22037
