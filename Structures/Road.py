import pygame
import logging

logging.basicConfig(level=logging.INFO, filename='Logs/debug.log', filemode='w')
logger = logging.getLogger(__name__)

from Structures.Structure import Structure
from Structures.Structure import Directions


class Road(Structure):
    height = 60

    def __init__(self, size, struct1: Structure, struct2: Structure, position, direction: int):
        super(Road, self).__init__(position, size, Road.height)
        logging.info("ROAD position: {0}, width:{1}, height:{2} ".format(position, self.width, self.height))
        self.removed = False
        # left / right
        size = int(size)
        self.buffers = [[False] * size, [False] * size]
        # left / right
        self.connected = [struct1, struct2]
        """:type : list[Structures.Structure.Structure]"""

        self.queue = [[], []]
        """:type : list[list[Movable.Car.Car]]"""
        self.position = position
        self.angle = 0 if direction < 2 else -90 + 180 * (direction - 2)
        self.image = pygame.Surface([self.width, self.height])

        self.image = pygame.transform.rotate(self.image, self.angle)

        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.updateNumber = 0

    @staticmethod
    def getMoveVector(dir, angle, speed):
        d = 1 if dir == Directions.Right else -1
        if angle == 0:
            return [speed * d, 0]
        if angle == -90:
            return [0, -speed * d]
        if angle == 90:
            return [0, speed * d]


    def register(self, car, dir: int):
        if dir == Directions.Right:
            self.registerRightByAngle(car)
        if dir == Directions.Left:
            car.rect.topleft = [self.position[0] + self.size + Road.heigth, self.position[1] + self.size - Road.heigth]
        self.enqueue(car, dir)

    def registerRightByAngle(self, car):
        car.rotate(self.angle)
        if self.angle == -90:  # down
            car.rect.topleft = [self.position[0] + car.rect.height, self.position[1]]
        if self.angle == 0:
            car.rect.topleft = [self.position[0], self.position[1] + Road.height / 2]
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
            print("REGISTERING")
            self.connected[dir].register(p, dir)

    def render(self, screen):
        screen.blit(self.image, self.rect)
        for mov in self.queue[0] + self.queue[1]:
            screen.blit(mov.image, mov.rect)

    def update(self):
        self.updateNumber += 1
        speed = 2
        self.updateBuffers(speed)
        for movable in self.queue[0]:
            movable.rect.move_ip(Road.getMoveVector(Directions.Right, self.angle, speed))
        for movable in self.queue[1]:
            movable.rect.move_ip(-speed, 0)

    def updateBuffers(self, speed):
        self.buffers[0] = [False] * speed + self.buffers[0]

        if self.buffers[0][-speed] and not self.removedRigth:
            self.removedRigth = True
            self.dequeue(0)
        elif not self.buffers[0][-speed]:
            self.removedRigth = False
        self.buffers[0] = self.buffers[0][:-speed]

        self.buffers[1] = [False] * speed + self.buffers[1]
        if self.buffers[1][-speed] and not self.removedLeft:
            self.removedLeft = True
            self.dequeue(1)
        elif not self.buffers[1][-speed]:
            self.removedLeft = False
        self.buffers[1] = self.buffers[1][:-speed]
