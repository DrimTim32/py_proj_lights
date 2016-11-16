import pygame
from Structures.Road import Road
from Movable.Car import Car
from Structures.CrossRoad import CrossRoad
from Structures.Elbow import Elbow
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
    car = Car((0, 10))
    # road = Road(300, None,None,[30,30])
    road = Elbow([0, 200], 300, 0, 3)
    road.register(car, 0)
    roads = [road]
    movable = [car]
    toRender = [road]
    """list[Structures.Elbow.Elbow]"""
    road.register(car, 1)
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.fill(Colors.gray)
        # update everything
        for road in roads:
            road.update()
        for mov in movable:
            mov.update()
        # move/color etc.

        for c in toRender:
            c.render(screen)
        pygame.draw.circle(screen, (0, 0, 255), road.structures[1].rect.topleft, 3)
        pygame.time.Clock().tick(30)
        pygame.display.flip()


if __name__ == "__main__":
    main()
