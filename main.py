import sys

import pygame

from Simulation import Game

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
    game = Game(screen)
    done = False
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        game.update()

        pygame.time.Clock().tick(1)
        pygame.display.flip()
    sys.exit()


if __name__ == "__main__":
    main()
