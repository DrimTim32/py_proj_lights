import pygame
from Structures.Structure import Structure
from Structures.Road import Road

import logging

logging.basicConfig(level=logging.INFO, filename='Logs/debug.log', filemode='w')
logger = logging.getLogger(__name__)


class Turn(Structure):
    def __init__(self, position: list, size: int, road1: Road, road2: Road) -> object:
        super(Turn, self).__init__(position, size, size)
        logging.info("TURN position: {0}, width:{1}, height:{2} ".format(position, self.width, self.height))
        self.buffers = [[False] * size, [False] * size]
        self.connected = [road1, road2]
        self.buffers = [[False] * size, [False] * size]

        self.connected = [road1, road2]
        self.queue = [[], []]
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.image.fill((0, 255, 0))

    def register(self, movable, dir):
        assert 0 <= dir <= 1
        self.buffers[dir] = list([True for i in range(movable.rect.width)]) + self.buffers[dir]
        self.queue[dir].append(movable)

    def dequeue(self, dir: int):
        assert 0 <= dir <= 1
        p = self.queue[dir].pop()
        if self.connected[dir] is not None:
            print(p.rect.topleft)
            self.connected[dir].register(p, dir)

    def render(self, screen):
        screen.blit(self.image, self.rect)
        for mov in self.queue[0] + self.queue[1]:
            screen.blit(mov.image, mov.rect)

    def update(self):
        self.updateBuffers()
        vect = (1, 0)

        for movable in self.queue[0]:
            if movable.rect.topleft >= (self.position[0], self.position[1]):
                movable.rect.move_ip(0, 1)
                if (movable.angle != self.connected[0].angle):
                    movable.rotate(self.connected[0].angle)
            else:
                movable.rect.move_ip(vect)
        for movable in self.queue[1]:
            movable.rect.move_ip(-vect[0], -vect[1])

    def updateBuffers(self):
        self.buffers[0] = [False] + self.buffers[0]

        if self.buffers[0][-1] and not self.removed:
            self.removed = True
            self.dequeue(0)
        elif not self.buffers[0][-1]:
            self.removed = False
        self.buffers[0].pop()

        self.buffers[1] = [False] + self.buffers[1]
        if self.buffers[1][-1] and not self.buffers[1][-2]:
            self.dequeue(1)
        self.buffers[1].pop()
