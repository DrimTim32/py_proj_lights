from collections import namedtuple

DirectionProperties = namedtuple('IntersectionProperties', ['in_width', 'out_width'])


class IntersectionProperties:
    def __init__(self, directions):
        self.width = 0
        self.height = 0
