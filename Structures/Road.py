import pygame
from Structures.Elbow import Elbow


class Road(Elbow):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.buffers = [[] * size, [] * size]
