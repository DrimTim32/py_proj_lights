import sys
from time import clock

import pygame

from core.configuration import config
from core.simulation import Game
from core.simulation.generators import CarProperGenerator
from core.simulation.lights_managers import FixedLightsManager

WINDOW_SIZE = (1000, 800)


def read_configuration():
    """Reads configuration from file"""
    return config.Config.from_config_file("Configuration/config.json")


def entrypoint():
    configuration = read_configuration()


def main():
    #   try:
    #        entrypoint()
    #   except Exception as e:
    #      print("{0}, message : {1}".format(sys.stderr, e))
    #     return 2

    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    prev_update_time = clock()
    done = False

    # Generators

    car_generator = CarProperGenerator()
    lights_manager = FixedLightsManager()

    game = Game(car_generator, lights_manager)
    game_map = game.map
    game_map.prepare(screen)
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        curr_time = clock()
        if curr_time - prev_update_time > 0.2:
            prev_update_time = curr_time
            game.update()

        game_map.draw(screen, game.points)

        pygame.time.Clock().tick(60)
        pygame.display.flip()
    sys.exit()


if __name__ == "__main__":
    main()
