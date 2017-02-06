import random
import operator
import time
from datetime import datetime
from math import log, sqrt, sin

from core.configuration.config import Config, SimulationData
import core.algorithms.algorithms as algorithms
from core.data_structures.enums import Orientation
from core.simulation import Simulation
from core.simulation.generators import CarProperGenerator
from core.simulation.lights_managers import LightsManager
from core.simulation.lights_managers.lights_phase import LightsPhase, DirectionsInfo


def read_configuration(config_path):
    """Reads configuration from file"""
    return Config.from_config_file(config_path)


def randomize_time():
    return random.randint(1, 2)


class Optimizer:
    min_lights_len = 10

    def __init__(self, config_path, car_generator=CarProperGenerator, lights_manager=LightsManager):
        self.config = read_configuration(config_path)
        self.car_generator = car_generator
        self.lights_manager = lights_manager

        self.norm = algorithms.get_norm(self.config.simulation_data.norm)
        self.car_importance = algorithms.get_importance(self.config.simulation_data.car_importance)
        self.time_importance = algorithms.get_importance(self.config.simulation_data.wait_time_importance)
        self.repetition_count = self.config.simulation_data.simulation_count

    @staticmethod
    def calcule_function(car_count, wait_count):
        return 1 / (car_count * car_count) * sin(wait_count / 1000)

    @staticmethod
    def generate_start_lights(count):
        return [20] * count

    def get_start_report(self, lights):
        data = self.config.simulation_data
        report_string = "Report generated {:%d, %b %Y}\n".format(datetime.now())
        report_string += "[Start Values]\n"
        report_string += "\tsimulation count =\n" + str(data.simulation_count)
        report_string += "\twait time importance =\n" + str(data.wait_time_importance)
        report_string += "\tcat count importance =\n" + str(data.car_importance)
        report_string += "\tgenerated lights =\n" + str(lights)
        report_string += "\tsimulation was executed {} times\n".format(data.simulation_count)
        report_string += "\teach simulation contained {} steps\n".format(data.step_count)
        return report_string

    def iterate_simulation(self, simulation, phrases):

        simulation.set_phases_durations(phrases)
        for _ in range(int(self.config.simulation_data.step_count)):
            simulation.update()
        data = simulation.current_data
        phase_count = len(data.items())
        vect = [0] * phase_count
        vector = [0] * phase_count
        car_sum, wait_sum = 0, 0
        for phase_no, j in data.items():
            car_count_list = [phase_data.car_count for phase_data in j]
            wait_count_list = [phase_data.average_waiting_time for phase_data in j]
            if car_count_list is None:
                car_count_list = []
            if wait_count_list is None:
                wait_count_list = []
            car_count = self.car_importance(car_count_list)
            wait_count = self.time_importance(wait_count_list)
            vector[phase_no] = self.calcule_function(car_count, wait_count)
            car_sum += sum(car_count_list)
            wait_sum += sum(wait_count_list)
            vect[phase_no] += vector[phase_no]
        simulation_norm = self.norm(vector)
        return simulation_norm, car_sum, wait_sum, vect

    @staticmethod
    def simulation_data_string(simulation_norm, car_sum, wait_sum):
        report_string = ""
        report_string += "\tcar passed: {}\n".format(car_sum)
        report_string += "\ttime wasted by being stopped: {}\n".format(wait_sum)
        report_string += "\taccomplished norm: {}\n".format(simulation_norm)
        return report_string

    @staticmethod
    def change_times(times, vect):
        max_index, value = max(enumerate(vect), key=operator.itemgetter(1))
        min_index, value = min(enumerate(vect), key=operator.itemgetter(1))
        times[max_index] -= randomize_time()
        if times[max_index] < Optimizer.min_lights_len:
            times[max_index] = Optimizer.min_lights_len
        times[min_index] += randomize_time()
        return times

    def simulate(self):
        simulation = Simulation(self.car_generator, self.lights_manager, self.config)
        phrases_count = simulation.get_number_of_phases()
        times = Optimizer.generate_start_lights(phrases_count)
        simulation.set_phases_durations(times)
        best_times = Optimizer.generate_start_lights(phrases_count)

        report_string = self.get_start_report(times)
        report_string += "[Initial data]\n"
        simulation_norm, car_sum, wait_sum, vect = self.iterate_simulation(simulation,
                                                                           Optimizer.generate_start_lights(
                                                                               phrases_count))
        report_string += Optimizer.simulation_data_string(simulation_norm, car_sum, wait_sum)
        report_string += "[Data after optimalization]\n"
        best_norm = simulation_norm
        best_cars, best_wait = car_sum, wait_sum
        times = Optimizer.change_times(times, vect)
        print("")
        count = int(self.config.simulation_data.simulation_count)
        for _ in range(count):
            simulation = Simulation(self.car_generator, self.lights_manager, self.config)
            simulation.set_phases_durations(times)
            simulation_norm, car_sum, wait_sum, vect = self.iterate_simulation(simulation,
                                                                               Optimizer.generate_start_lights(
                                                                                   phrases_count))
            if simulation_norm < best_norm:
                best_norm = simulation_norm
                best_cars = car_sum
                best_wait = wait_sum
                best_times = [t for t in times]

            for i in range(len(best_times)):
                times[i] = best_times[i]
            times = Optimizer.change_times(times, vect)
            print("\r {}/{} simulation loops done".format(_, count), end="")
        report_string += Optimizer.simulation_data_string(best_norm, best_cars, best_wait)
        print("")
        print(report_string)
        print("New times ", times)


opt = Optimizer("../simple_config.json")
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


def choose_wait_count(count1, count2):
    return (count2 + count1) / 2


def choose_car_count(count1, count2):
    return count1 + count2


def main():
    car_generator = CarProperGenerator
    lights_manager = LightsManager
    N = 500
    times, best_times, = [30] * 4, [30] * 4
    best_norm = 99999999999
    best_cars, best_wait = 0, 0
    with open('test12.txt', 'w') as file:
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
