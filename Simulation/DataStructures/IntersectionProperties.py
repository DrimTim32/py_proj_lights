from collections import namedtuple

DirectionProperties = namedtuple('DirectionProperties', ['in_width', 'out_width'])


class IntersectionProperties:
    def __init__(self, directions):
        self.top = directions[0]
        self.left = directions[1]
        self.bottom = directions[2]
        self.right = directions[3]
        self.directions = directions
        self.width = max(self.top.in_width + self.top.out_width,
                         self.bottom.in_width + self.bottom.out_width)
        self.height = max(self.left.in_width + self.left.out_width,
                          self.right.in_width + self.right.out_width)
