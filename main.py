import sys
from time import clock

import pygame

from Drawing import Renderer
from Simulation import CarRandomGenerator
from Simulation import FixedLightsManager
from Simulation import Game

# consts

windowSize = (1000, 800)


class Colors:
    gray = (211, 211, 211)
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)


def main():
    pygame.init()

    screen = pygame.display.set_mode(windowSize)
    car_generator = CarRandomGenerator()
    lights_manager = FixedLightsManager()
    game = Game(car_generator, lights_manager)
    renderer = Renderer(screen)
    prev_update_time = clock()
    done = False
    render_list = [game.map]
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        curr_time = clock()
        if curr_time - prev_update_time > 0.2:
            prev_update_time = curr_time
            render_list = game.update()

        renderer.render(render_list)

        pygame.time.Clock().tick(60)
        pygame.display.flip()
    sys.exit()


if __name__ == "__main__":
    main()
