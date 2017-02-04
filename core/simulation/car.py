class Car:
    def __init__(self, source, turn_direction):
        self.source = source
        self.turn_direction = turn_direction
        self.destination = (self.source + self.turn_direction) % 4
        self.waiting_time = 0
