class Intersection:
    def __init__(self, properties):
        self.array = [[None for _ in range(properties.width)] for _ in range(properties.height)]

    def pull_car(self, direction=0, lane=0):
        return 0
        # return random.choice([0 for _ in range(direction + 3)] + [1])

    def push_car(self, direction=0, lane=0):
        print('car_pushed ', direction, lane)
