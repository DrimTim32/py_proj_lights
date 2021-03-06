"""This file contains main example of the project"""
import sys
from time import clock

import pygame

from algorithms.optimiser import Optimiser
from configuration import config
from simulation.generators.car_proper_generator import CarProperGenerator
from simulation.lights_managers.lights_manager import LightsManager
from simulation.simulation import Simulation

WINDOW_SIZE = (1000, 800)


def read_configuration(path):
    """Reads configuration from file in path"""
    return config.Config.from_config_file(path)


def entry_point(path):
    """
    Entry point for application
    """

    configuration = read_configuration(path)
    print("Configuration readed succesfully.")

    car_generator = CarProperGenerator
    lights_manager = LightsManager

    optimizer = Optimiser(configuration, car_generator, lights_manager)
    print("Starting optimization.")
    report_string, times = optimizer.optimise()
    print("")
    print(report_string)
    print("New times ", times)

    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    prev_update_time = clock()

    simulation = Simulation(car_generator, lights_manager, configuration)  # type: Simulation
    simulation.set_phases_durations(times)
    game_map = simulation.map
    lights_painter = simulation.map.get_lights_painter()
    game_map.prepare(screen)

    done = False
    while not done:
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            done = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        curr_time = clock()
        if curr_time - prev_update_time > 0.2:
            prev_update_time = curr_time
            simulation.update()

        game_map.draw(screen, simulation.points)
        lights_painter.draw(screen, simulation.get_lights())

        pygame.time.Clock().tick(60)
        pygame.display.flip()
    sys.exit()


def main():
    """This is main method for this file"""
    path = "config.json"
    if len(sys.argv) < 2:
        print("Configuration file is not provided, using default.")
    else:
        path = sys.argv[1]
    entry_point(path)
    try:
        pass
    except Exception as exc:
        print("{0}, message : {1}".format(sys.stderr, exc))
        return 2


if __name__ == "__main__":
    main()
