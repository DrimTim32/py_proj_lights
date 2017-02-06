import numpy as np
import numpy.linalg as la


def metric_euclid(vector):
    return la.norm(vector)


def metric_min(vector):
    return la.norm(vector, np.inf)


def metric_max(vector):
    return la.norm(vector, -np.inf)


def _sum(vector):
    return sum(vector)


def avg(vector):
    if len(vector) == 0:
        return 0
    return sum(vector) / len(vector)


metrics = {
    "euclid": metric_euclid,
    "inf": metric_max,
    "-inf": metric_min
}
importance = {
    "sum": _sum,
    "avg": avg
}


def get_norm(name):
    if name in metrics.keys():
        return metrics[name]
    raise ValueError("Name '{}' does not stand for any known metric", name)


def get_importance(name):
    if name in importance.keys():
        return importance[name]
    raise ValueError("Name '{}' does not stand for any known importance", name)
