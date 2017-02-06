import numpy as np
import numpy.linalg as la


def metric_euclid(vector):
    return la.norm(vector)


def metric_min(vector):
    return la.norm(vector, np.inf)


def metric_max(vector):
    return la.norm(vector, -np.inf)


metrics = {
    "euclidean": metric_euclid,
    "inf": metric_max,
    "-inf": metric_min
}


def norm(name):
    if name in metrics.keys():
        return metrics[name]
    raise ValueError("Name '{}' does not stand for any known metric", name)
