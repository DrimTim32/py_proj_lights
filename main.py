import sys
from time import clock
import pygame

from Simulation import CarRandomGenerator
from Simulation import FixedLightsManager
from Simulation import Game


windowSize = (1000, 800)


def main():
    pygame.init()

    screen = pygame.display.set_mode(windowSize)
    prev_update_time = clock()
    done = False

    #Generators
    car_generator = CarRandomGenerator()
    lights_manager = FixedLightsManager()

    game = Game(car_generator, lights_manager)
    map = game.map
    map.prepare(screen)
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

        map.draw(screen,game.points)

        pygame.time.Clock().tick(60)
        pygame.display.flip()
    sys.exit()


if __name__ == "__main__":
    main()
