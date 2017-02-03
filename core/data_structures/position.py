class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __ne__(self, other):
        return not (self == other)

    def __eq__(self, other):
        return self is other or (self.x == other.x and self.y == other.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Position ({0},{1})".format(self.x, self.y)

    def __getitem__(self, item):
        return self.x if item == 0 else self.y

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def copy(self):
        return Position(self.x, self.y)

    def __neg__(self):
        return Position(-self.x, -self.y)
