import pygame
from Structures.Structure import Structure
from Structures.Road import Road


class Turn(Structure):
    def __init__(self, position: list, size: int, road1: Road, road2: Road) -> object:
        super(Turn, self).__init__(position, size, size)
        self.buffers = [[False] * size, [False] * size]
        self.connected = [road1, road2]
        self.buffers = [[False] * size, [False] * size]

        self.connected = [road1, road2]
        self.queue = [[], []]
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.image.fill((255, 0, 0))

    def register(self, movable, dir):
        pass

    def render(self, screen):
        screen.blit(self.image, self.rect)
        for mov in self.queue[0] + self.queue[1]:
            screen.blit(mov.image, mov.rect)
