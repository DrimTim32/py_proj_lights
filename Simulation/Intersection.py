class IntersectionProperties:
    def __init__(self, directions):
        self.top = directions[0]
        self.left = directions[1]
        self.bottom = directions[2]
        self.right = directions[3]
        self.directions = directions
        self.width = max(self.top.in_lanes_count + self.top.out_lanes_count,
                         self.bottom.in_lanes_count + self.bottom.out_lanes_count)
        self.height = max(self.left.in_lanes_count + self.left.out_lanes_count,
                          self.right.in_lanes_count + self.right.out_lanes_count)


class Intersection:
    def __init__(self, properties):
        self.array = [[1 for _ in range(properties.width)] for _ in range(properties.height)]

    def pull_car(self, direction=0, lane=0):
        return 0
        # return random.choice([0 for _ in range(direction + 3)] + [1])

    def push_car(self, direction=0, lane=0):
        print('car_pushed ', direction, lane)
