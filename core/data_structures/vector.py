"""This file contains Position class"""


class Vector:
    """ Vector class represents and manipulates x,y coords. """

    def __init__(self, x, y):
        """ Create a new point """
        self.x = x
        self.y = y

    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError("Second multiplication object must be an int")
        return Vector(self.x * other, self.y * other)

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        return self is other or (self.x == other.x and self.y == other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Position ({0},{1})".format(self.x, self.y)

    def __getitem__(self, item):
        return self.x if item == 0 else self.y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def copy(self):
        """
        Creates new object with the same position
        :rtype: Vector
        """
        return Vector(self.x, self.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)
