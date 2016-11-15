import pygame


def angle(A):
    A = list(A)
    if A[0] == 0 and A[1] == 0:
        return 0
    if A[0] == 0 and A[1] >= 1:
        return -90
    if A == [1, 1]:
        return -45
    if A == [0, -1]:
        return 90
    # TODO : more angles?
    return 0


class Car(pygame.sprite.Sprite):
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
        self.lastRotation = 0

    def rotate(self, vector):
        """ Rotates image depending on move vector
        >>> rotate([0,1])
        rotates to the west
        >>> rotate([0,-1])
        rotates to the north
        """
        if vector == (0, 0):
            return
        self.image = pygame.transform.rotate(self.image, -self.lastRotation)
        self.lastRotation = angle(vector)
        self.image = pygame.transform.rotate(self.image, self.lastRotation)

    def move(self, vector):
        """ Moves a car by vector. Care with [1,1] """
        if vector[0] == 0 and vector[1] == 0:
            return
        self.rotate(vector)
        # temporary solution
        self.rect.move_ip(vector[0], vector[1])

    # what is going on every frame
    def update(self):
        pass
