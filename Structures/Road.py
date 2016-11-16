import pygame
from Structures.CrossRoad import CrossRoad
from Structures.Structure import Structure
from Structures.Structure import Directions


class Road(Structure):
    carSize = 10
    height = 60

    def __init__(self, size, struct1: Structure, struct2: Structure, position, direction: int):
        super(Road, self).__init__(position, size, Road.height)
        # left / right
        size = int(size)
        self.buffers = [[False] * size, [False] * size]
        # left / right
        self.connected = [struct1, struct2]
        """:type : list[Structures.Structure.Structure]"""

        self.queue = [[], []]
        """:type : list[list[Movable.Car.Car]]"""
        self.position = position
        angle = 0 if direction < 2 else -90 + 180 * (direction - 2)
        print(angle)
        self.image = pygame.Surface([self.width, self.height])

        self.image = pygame.transform.rotate(self.image, angle)

        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.updateNumber = 0

    def register(self, car, dir: int):
        print("Registered")
        if dir == Directions.Right:
            car.rect.topleft = [self.position[0], self.position[1] + self.heigth / 2]
        if dir == Directions.Left:
            car.rect.topleft = [self.position[0] + self.size + self.heigth, self.position[1] + self.size - self.heigth]
        self.enqueue(car, dir)

    def enqueue(self, car, dir: int):
        assert 0 <= dir <= 1
        self.queue[dir].append(car)
        buf = self.buffers[dir]
        for i in range(car.rect.width):
            buf[i] = True

    def dequeue(self, dir: int):
        assert 0 <= dir <= 1
        p = self.queue[dir].pop()
        if self.connected[dir] is not None:
            self.connected[dir].register(p)

    def render(self, screen):
        screen.blit(self.image, self.rect)
        for mov in self.queue[0] + self.queue[1]:
            screen.blit(mov.image, mov.rect)

    def update(self):
        self.updateNumber += 1
        self.updateBuffers()
        for movable in self.queue[0]:
            movable.rect.move_ip(1, 0)
        for movable in self.queue[1]:
            movable.rect.move_ip(-1, 0)

    def updateBuffers(self):
        self.buffers[0] = [False] + self.buffers[0]
        if self.buffers[0][-1] and not self.buffers[0][-2]:
            self.dequeue(0)
        self.buffers[0].pop()

        self.buffers[1] = [False] + self.buffers[1]
        if self.buffers[1][-1] and not self.buffers[1][-2]:
            self.dequeue(1)
        self.buffers[1].pop()
