import pygame
from Structures.Road import Road
from Movable.Car import Car
from Structures.CrossRoad import CrossRoad
# consts
windowSize = (800, 600)


class Colors:
    gray = (211, 211, 211)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)


def main():
    pygame.init()

    screen = pygame.display.set_mode(windowSize)
    done = False
    car = Car((10, 10))
    cross = [CrossRoad(), CrossRoad()]
    road = Road(10, cross[0], cross[1])
    roads = [road]
    movable = [car]
    toRender = [car]
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # update everything
        for road in roads:
            road.update()
        for mov in movable:
            mov.update()
        # move/color etc.
        screen.fill(Colors.gray)

        for c in toRender:
            screen.blit(c.image, c.rect)

        pygame.time.Clock().tick(30)
        pygame.display.flip()


if __name__ == "__main__":
    main()
