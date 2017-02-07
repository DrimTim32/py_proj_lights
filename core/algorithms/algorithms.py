"""This file contains algorithms used in optimizer"""
import numpy as np
import numpy.linalg as la
import math


def metric_euclid(vector):
    return la.norm(vector)


def norm_min(vector):
    return la.norm(vector, -np.inf)


def norm_max(vector):
    """Returns minimum norm from vector"""
    return la.norm(vector, np.inf)


def avg(vector):
    """Returns average of the vector"""
    if len(vector) == 0:
        return 0
    return sum(vector) / len(vector)


def logistic(x, top, var1, var2):
    return top / (1 + math.exp(-(x - var1) / var2))


def gompertz(x, top, var1, var2):
    return top - top * math.exp((-var1 * math.exp(-var2 * x)))


metrics = {
    "euclid": metric_euclid,
    "inf": norm_max,
    "-inf": norm_min
}


def get_norm(name):
    if name in metrics.keys():
        return metrics[name]
    raise ValueError("Name '{}' does not stand for any known metric", name)