"""This file contains algorithms used in optimizer"""
import math

import numpy as np
import numpy.linalg as la


def metric_euclid(vector):
    """Returns euclidean norm from vector"""
    return la.norm(vector)


def norm_min(vector):
    """Returns minimum norm from vector"""
    return la.norm(vector, -np.inf)


def norm_max(vector):
    """Returns maximum norm from vector"""
    return la.norm(vector, np.inf)


def avg(vector):
    """Returns average of the vector"""
    if len(vector) == 0:
        return 0
    return sum(vector) / len(vector)


def logistic(x_0, max_value, midpoint, steepness):
    """
    Logistic cumulative distribution curve
    :param x_0: point where function is going to be calculated
    :param max_value: function max value
    :param midpoint: midpoint
    :param steepness: how much function shoud be steep
    :return:
    """
    return max_value / (1 + math.exp(-(x_0 - midpoint) / steepness))


def negative_gompertz(x_0, asymptote, inflection, rate):
    """
    Negative gompertz function.
    :param x_0: point where function is going to be calculated
    :param asymptote: curve asymptote
    :param inflection: inflection of the curve
    :param rate: rate parameter
    :type x_0: float
    :type asymptote: float
    :type inflection: float
    :type rate: float
    :rtype: float
    """
    return 1 - asymptote * math.exp((-inflection * math.exp(-rate * x_0)))


def get_norm(name):
    """Returns norm by string"""
    if name in _metrics.keys():
        return _metrics[name]
    raise ValueError("Name '{}' does not stand for any known norm", name)


_metrics = {
    "euclid": metric_euclid,
    "inf": norm_max,
    "-inf": norm_min
}
