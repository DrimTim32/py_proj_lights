import random
import operator
import time
from datetime import datetime
from math import log, sqrt, sin, e
import numpy as np

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
    return random.randint(1, 10)


class Optimizer:
    min_lights_len = 10

    def __init__(self, config_path, car_generator=CarProperGenerator, lights_manager=LightsManager):
        self.config = read_configuration(config_path)
        self.car_generator = car_generator
        self.lights_manager = lights_manager

        self.norm = algorithms.get_norm(self.config.simulation_data.norm)
        self.car_importance = algorithms.avg
        self.time_importance = sum
        self.repetition_count = self.config.simulation_data.simulation_count

    def gompertz_car(self, x):
        return 1 - 0.9 * pow(e, (-5 * pow(e, -0.005 * x)))

    def gompertz_time(self, x):
        q = 0.9 * pow(e, (-5 * pow(e, -0.005 * x)))
        return q

    def calcule_function(self, car_count, wait_count):
        return self.gompertz_car(car_count) * self.gompertz_time(wait_count)

    @staticmethod
    def generate_start_lights(count):
        return [20] * count

    def get_start_report(self, lights):
        data = self.config.simulation_data
        report_string = "Report generated {:%d, %b %Y}\n".format(datetime.now())
        report_string += "[Start Values]\n"
        report_string += "\tsimulation count = {} \n".format(str(data.simulation_count))
        report_string += "\tgenerated lights = {} \n".format(str(lights))
        report_string += "\tsimulation was executed {} times\n".format(data.simulation_count)
        report_string += "\teach simulation contained {} steps\n".format(data.step_count)
        return report_string

    def iterate_simulation(self, simulation, phrases):
        simulation.set_phases_durations(phrases)
        for _ in range(int(self.config.simulation_data.step_count)):
            simulation.update()
        data = simulation.current_data
        phase_count = simulation.get_number_of_phases()
        vect = [0] * phase_count
        vector = [0] * phase_count
        car_sum, wait_sum = 0, 0
        for phase_no, j in data.items():
            car_count_list = [phase_data.car_count for phase_data in j]
            wait_count_list = [phase_data.total_waiting_time for phase_data in j]
            if car_count_list is None:
                car_count_list = []
            if wait_count_list is None:
                wait_count_list = []
            car_count = self.car_importance(car_count_list)
            wait_count = self.time_importance(wait_count_list) / int(self.config.simulation_data.step_count)
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
        # report_string += Optimizer.simulation_data_string(simulation_norm, car_sum, wait_sum)
        report_string += "[Data after optimalization]\n"
        best_norm = simulation_norm
        best_cars, best_wait = car_sum, wait_sum
        times = Optimizer.change_times(times, vect)

        count = int(self.config.simulation_data.simulation_count)
        for q in range(count):
            try:
                simulation = Simulation(self.car_generator, self.lights_manager, self.config)
                simulation.set_phases_durations(times)
                simulation_norm, car_sum, wait_sum, vect = self.iterate_simulation(simulation, times)
                if simulation_norm < best_norm:
                    best_norm = simulation_norm
                    best_cars = car_sum
                    best_wait = wait_sum
                    best_times = [t for t in times]
                report_string += Optimizer.simulation_data_string(simulation_norm, car_sum, wait_sum)
                for i in range(len(best_times)):
                    times[i] = best_times[i]
                times = Optimizer.change_times(times, vect)
                print("\r {}/{} simulation loops done".format(q + 1, count), end="")
            except Exception as ex:
                q -= 1
                continue
        report_string += Optimizer.simulation_data_string(best_norm, best_cars, best_wait)
        print("")
        print(report_string)
        print("New times ", times)


opt = Optimizer("../simple_config.json")
opt.simulate()
