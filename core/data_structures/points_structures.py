"""This file contains point structures used in the project"""
from collections import namedtuple

PointsQuadruple = namedtuple('PointsQuadruple', ['top', 'left', 'down', 'right'])
RoadPointsGroup = namedtuple('RoadPointsGroup', ['outside', 'inside'])
PointsPair = namedtuple('PointsPair', ['start', 'end'])
