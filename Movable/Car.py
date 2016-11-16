import pygame


class Car(pygame.sprite.Sprite):
    """
    :type image: pygame.Image
    """
    image = None
    speed = 2

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        # load image (pseudo static)
        if Car.image is None:
            Car.image = pygame.image.load("images/car.gif")
        self.image = Car.image
        self.image.set_colorkey((255, 255, 255))  # tlo
        self.rect = self.image.get_rect()
        self.location = location
        self.rect.topleft = location

    def move(self, vector):
        """ Moves a car by vector. Care with [1,1] """
        if vector[0] == 0 and vector[1] == 0:
            return
        # temporary solution
        self.rect.move_ip(vector[0], vector[1])

    # what is going on every frame
    def update(self):
        pass
