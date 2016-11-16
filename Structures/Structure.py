import pygame


class Structure(pygame.sprite.Sprite):
    def __init__(self, position, width, heigth):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.width = width
        self.height = heigth

    def render(self, screen):
        pass

    def register(self, movable, dir: int):
        pass

    def update(self):
        super().update()

class Directions:
    Right = 0
    Left = 1
    Up = 2
    Down = 3
