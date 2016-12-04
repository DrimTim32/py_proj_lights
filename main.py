import pygame
import sys
from Drawing import Map

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
    map = Map()
    done = False
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        map.prepare(screen)
        map.draw(screen)
        pygame.time.Clock().tick(15)
        pygame.display.flip()
    sys.exit()

if __name__ == "__main__":
    main()
