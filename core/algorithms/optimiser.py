"""This file contains optimiser class"""
from __future__ import print_function

import operator
import random
import sys
from collections import namedtuple
from datetime import datetime

from simulation import Simulation
from .algorithms import avg, get_norm, negative_gompertz, logistic
from .algorithms_exceptions import OptimisationException

SimulationData = namedtuple('SimulationData', ['norm', 'car_sum', 'wait_sum', 'vect'], False)  # pylint: disable=C0103


class Optimiser:
    """This class is tool for optimising crossroads"""
    min_lights_len = 2
    max_lights_len = 64

    def __init__(self, config, car_generator, lights_manager):
        self.config = config
        self.car_generator = car_generator
        self.lights_manager = lights_manager
        self.norm = get_norm('euclid')
        self.repetition_count = self.config.simulation_data.simulation_count
        self.max_possible_wait_time = self.config.simulation_data.step_count - self.config.roads_length
        self.max_possible_car_count = self.config.simulation_data.step_count
        self.init_values = Optimiser.max_lights_len // 2
        self.max_random_change = self.init_values // 2

    def __randomize_time_change(self):
        """
        Randomizes time change
        :rtype: int
        """
        return random.randint(1, self.max_random_change)

    def __car_equation(self, point):
        """
        Returns car curve value
        :param point: point where curve should be calculated
        :type point: float
        :rtype: float
        """
        return negative_gompertz(point, 1.0, 5.0, 5.0 / self.config.simulation_data.step_count)

    def __time_equation(self, point):
        """
        Returns time curve value
        :param point: point where curve should be calculated
        :type point: float
        :rtype: float
        """
        return logistic(point, 1.0, (self.config.simulation_data.step_count / 2.0),
                        (self.config.simulation_data.step_count / 10.0))

    def __calcule_function(self, car_count, wait_count):
        """
        Calculates characteristic function
        :param car_count: car count value
        :param wait_count: wait count value
        :type car_count: float
        :type wait_count: float
        :rtype: float
        """
        return self.__car_equation(car_count) + self.__time_equation(wait_count)

    def __generate_start_lights(self, count):
        """
        Generates start lights
        :param count: count of lights
        :type count: int
        :rtype list[int]
        """
        return [self.init_values] * count

    def __get_start_report(self, lights):
        """
        Generates start report
        :param lights: lights values list
        :type lights: list[int]
        :rtype: str
        """
        data = self.config.simulation_data
        report_string = "Report generated {:%d, %b %Y}\n".format(datetime.now())
        report_string += "[Start Values]\n"
        report_string += "\tsimulation count = {} \n".format(str(data.simulation_count))
        report_string += "\tgenerated lights = {} \n".format(str(lights))
        report_string += "\tsimulation was executed {} times\n".format(data.simulation_count)
        report_string += "\teach simulation contained {} steps\n".format(data.step_count)
        return report_string

    def __iterate_simulation(self, simulation, lights):
        """
        Simulates one simulation
        :param simulation: simulation object
        :type simulation: Simulation
        :param lights: list of lights times
        :type lights: list[int]
        :return:
        """
        simulation.set_phases_durations(lights)
        for _ in range(self.config.simulation_data.step_count):
            simulation.update()
        data = simulation.current_data  # type: dict[int, list[LanePhaseData]]
        phase_count = simulation.get_number_of_phases()
        vect = [0] * phase_count
        vector = [0] * phase_count
        car_sum, wait_sum = 0, 0
        for phase_no, phase_data in data.items():
            car_count_list = [data.car_count for data in phase_data]
            wait_count_list = [data.average_waiting_time for data in phase_data]
            if car_count_list is None:
                car_count_list = []
            if wait_count_list is None:
                wait_count_list = []
            car_count = avg(car_count_list)
            wait_count = avg(wait_count_list)
            vector[phase_no] = self.__calcule_function(car_count, wait_count)
            vect[phase_no] += vector[phase_no]
            car_sum += sum(car_count_list)
            wait_sum += sum([data.total_waiting_time for data in phase_data])
        return SimulationData(self.norm(vector), car_sum, wait_sum, vect)

    @staticmethod
    def __simulation_data_string(simulation_data):
        """
        Generates string from simulation data
        :param simulation_data: simulation data
        :type simulation_data: SimulationData
        :rtype: str
        """
        report_string = ""
        report_string += "\tcar passed: {}\n".format(simulation_data.car_sum)
        report_string += "\ttime wasted by being stopped: {}\n".format(simulation_data.wait_sum)
        report_string += "\taccomplished norm: {}\n".format(simulation_data.norm)
        return report_string

    def __change_times(self, times, vect):
        """
        Changes times based on vector
        :param times: light times
        :type times: list[int]
        :param vect: vector
        :type vect: list[float]
        :rtype : list[int]
        """
        max_index = max(enumerate(vect), key=operator.itemgetter(1))[0]
        min_index = min(enumerate(vect), key=operator.itemgetter(1))[0]
        times[max_index] -= self.__randomize_time_change()
        times[min_index] += self.__randomize_time_change()
        times[max_index] = max(Optimiser.min_lights_len, times[max_index])
        times[min_index] = min(times[min_index], Optimiser.max_lights_len)
        return times

    def optimise(self):
        """
        Optimises simulation
        :return: report with most optimal light phases
        :rtype: tuple(string,list[int])
        """
        better_count = 0
        bad_simulation = 0
        last_exception = None

        simulation = Simulation(self.car_generator, self.lights_manager, self.config)
        times = self.__generate_start_lights(simulation.get_number_of_phases())
        best_times = self.__generate_start_lights(simulation.get_number_of_phases())

        simulation.set_phases_durations(times)
        report_string = self.__get_start_report(times)
        report_string += "[Initial data]\n"
        if sys.version_info[0] != 3:
            print("Data about progress is not aviable in python < 3.3 because of flush performance")
        print("Executing initial simulation", end="\r")
        print("" + "" * 50)
        simulation_data = self.__iterate_simulation(simulation, times)

        report_string += Optimiser.__simulation_data_string(simulation_data)
        report_string += "[Data after optimalization]\n"
        best_simulation_data = SimulationData(
            simulation_data.norm, simulation_data.car_sum, simulation_data.wait_sum,
            simulation_data.vect)  # type: SimulationData
        times = self.__change_times(times, simulation_data.vect)

        count = int(self.config.simulation_data.simulation_count)

        for i in range(count):
            if bad_simulation > 10:
                raise OptimisationException(
                    "Something wrong happend more than {} times, latest cought exception : {}".format(bad_simulation,
                                                                                                      last_exception))
            try:
                simulation = Simulation(self.car_generator, self.lights_manager, self.config)
                simulation.set_phases_durations(times)
                current_simulation_data = self.__iterate_simulation(simulation, times)

                if current_simulation_data.norm < best_simulation_data.norm:
                    best_simulation_data = SimulationData(
                        current_simulation_data.norm, current_simulation_data.car_sum, current_simulation_data.wait_sum
                        , current_simulation_data.vect)
                    best_times = [t for t in times]
                    better_count += 1
                for j in range(len(best_times)):
                    times[j] = best_times[j]
                times = self.__change_times(times, best_simulation_data.vect)
                print("\r{0:.0f}% of optimisation done".format(((i + 1) / count) * 100), end="")
            except Exception as ex:
                last_exception = ex
                bad_simulation += 1
                i -= 1
                continue
        report_string += Optimiser.__simulation_data_string(best_simulation_data)
        report_string += "[Additional data]\n\tNew norm was choosen {} times\n".format(better_count)
        return report_string, times
