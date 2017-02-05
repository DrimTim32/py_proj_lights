import random
import operator
import time
from math import log, sqrt

from core.configuration import config
from core.data_structures.enums import Orientation
from core.simulation import Simulation
from core.simulation.generators import CarProperGenerator
from core.simulation.lights_managers import LightsManager
from core.simulation.lights_managers.lights_phase import LightsPhase, DirectionsInfo


def read_configuration(config_path):
    """Reads configuration from file"""
    return config.Config.from_config_file(config_path)


class OptimalizerCreator:
    pass


class Optimizer:
    def __init__(self, config_path, car_generator=CarProperGenerator, lights_manager=LightsManager):
        self.config = read_configuration(config_path)
        self.car_generator = car_generator
        self.lights_manager = lights_manager

    @staticmethod
    def generate_start_lights(count):
        return [20]*count

    def simulate(self):
        simulation = Simulation(self.car_generator, self.lights_manager, self.config)
        lights = simulation.current_data
        print(lights)
        times = Optimizer.generate_start_lights(4)


opt = Optimizer("../config.json")
opt.simulate()

def norm(vector):
    from numpy.linalg import norm
    return norm(vector)


def get_lights(times):
    t1, t2, t3, t4 = times
    return [LightsPhase(DirectionsInfo(True, True, False, False), Orientation.VERTICAL, t1),
            LightsPhase(DirectionsInfo(False, False, False, True), Orientation.VERTICAL, t2),
            LightsPhase(DirectionsInfo(True, True, False, False), Orientation.HORIZONTAL, t3),
            LightsPhase(DirectionsInfo(False, False, False, True), Orientation.HORIZONTAL, t4)]


def randomize_time():
    return random.randint(1, 7)


def choose_wait_count(count1, count2):
    return (count2 + count1) / 2


def choose_car_count(count1, count2):
    return count1 + count2


def calcule_function(car_count, wait_count):
    return 1 / log(sqrt(car_count))  # * log(wait_count)


def main():
    car_generator = CarProperGenerator
    lights_manager = LightsManager
    N = 500
    times, best_times, = [30] * 4, [30] * 4
    best_norm = 99999999999
    best_cars, best_wait = 0, 0
    with open('test12.txt', 'w') as file:
        start = time.time()
        file.write("Metric: euclid\n")
        file.write("Main function: ")
        file.write("1/log(car_count,100) * log(wait_count,1000)\n")
        file.write("Car count choosing: sum\n")
        file.write("Wait time count choosing: avg\n")
        file.write("Start values: N={}, light times{}\n".format(N, times))
        file.write("After first iteration\n")
        for z in range(N):
            vect = [0, 0, 0, 0]
            game = Simulation(car_generator, lights_manager)
            game.lights_manager.phases = get_lights(times)
            for _ in range(300):
                game.update()
            data = game.get_current_data()
            car_sum = 0
            wait_sum = 0
            vector = [0, 0, 0, 0]
            for k, j in data.items():
                if len(j) != 2:
                    vect = -1
                    print("dupa")
                    break
                car_count = j[0].car_count + j[1].car_count
                wait_count = choose_wait_count(j[0].average_waiting_time, j[1].average_waiting_time)
                vector[k] = calcule_function(car_count, wait_count)
                car_sum += j[0].car_count + j[1].car_count
                wait_sum += j[0].average_waiting_time + j[1].average_waiting_time
                vect[k] += vector[k]
            if vect == -1:
                continue
            simulation_norm = norm(vector)
            if simulation_norm < best_norm:
                best_norm = simulation_norm
                best_cars = car_sum
                best_wait = wait_sum
                best_times = [t for t in times]

            for i in range(len(best_times)):
                times[i] = best_times[i]
            max_index, value = max(enumerate(vect), key=operator.itemgetter(1))
            min_index, value = min(enumerate(vect), key=operator.itemgetter(1))
            times[max_index] -= randomize_time()
            times[min_index] += randomize_time()
            if z == 0:
                file.write("Car sum {}, sum wait {}, norm {}\n".format(best_cars, best_wait, best_norm))
            print("z = ", z)
        end = time.time()
        file.write("BEST\n")
        file.write("Car sum {}, sum wait {}, norm {}\n".format(best_cars, best_wait, best_norm))
        file.write("New times {}\n".format(best_times))
        file.write("Experiment took {}".format(end - start))

