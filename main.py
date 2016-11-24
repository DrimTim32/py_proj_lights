import pygame
from Structures.Road import Road, RoadNode
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
    road = Road([100, 100])
    i = 1
    while i < 10000:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if i % 10 == 0 and i % 3 != 0:
            road.addCar()
        screen.fill(Colors.gray)
        # update everything
        road.render(screen)
        # print("Printing list data:")
        road.printList()
        road.refresh()
        # move/color etc.
        pygame.time.Clock().tick(15)
        pygame.display.flip()
        i +=1

if __name__ == "__main__":
    main()
