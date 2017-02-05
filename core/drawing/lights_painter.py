from core.data_structures.vector import Vector
from core.drawing.drawing_consts import LIGHT_OFFSET, LIGHT_RADIUS
from core.drawing.drawing_helpers import draw_circle
from core.drawing.drawing_consts import GREEN, RED
from core.data_structures.enums import Directions
from collections import namedtuple

"""Structure for lists of colors"""
RoadColorsVector = namedtuple('ColorsVector', ['top', 'left', 'bottom', 'right'])


class LightsPainter:
    def __init__(self, top_location, left_location, bottom_location, right_location):
        """
        :param top_location: upper lights location start
        :param left_location: left lights location start
        :param bottom_location: bottom lights location start
        :param right_location: right lights location start
        :type top_location: Vector
        :type left_location: Vector
        :type bottom_location: Vector
        :type right_location: Vector
        """
        self.__top_vector = Vector(0, -(LIGHT_OFFSET + LIGHT_RADIUS))
        self.__left_vector = Vector(-(LIGHT_OFFSET + LIGHT_RADIUS), 0)
        self.__down_vector = Vector(0, (LIGHT_OFFSET + LIGHT_RADIUS))
        self.__right_vector = Vector((LIGHT_OFFSET + LIGHT_RADIUS), 0)

        self.__top_location = top_location + self.__top_vector + self.__left_vector
        self.__left_location = left_location + self.__down_vector + self.__left_vector
        self.__bottom_location = bottom_location + self.__down_vector + self.__right_vector
        self.__right_location = right_location + self.__top_vector + self.__right_vector

    def draw(self, screen, lights_dict):
        for direction, lights in lights_dict.items():
            self.__draw(screen, direction, lights)

    def __draw(self, screen, direction, vector):
        vector = vector[::-1]
        if direction == Directions.BOTTOM:
            self.__draw_bottom(screen, vector)
        if direction == Directions.TOP:
            self.__draw_top(screen, vector)
        if direction == Directions.RIGHT:
            self.__draw_right(screen, vector)
        if direction == Directions.LEFT:
            self.__draw_left(screen, vector)

    def __draw_top(self, screen, array):
        """
        :param screen:
        :param array:
        :type colors_vector: RoadColorsVector
        :return:
        """
        for i in range(len(array)):
            color = GREEN if array[i] else RED
            draw_circle(screen, self.__top_location + 2 * i * self.__left_vector, LIGHT_RADIUS, color)

    def __draw_left(self, screen, array):
        """

        :param screen:
        :param array:
        :type colors_vector: RoadColorsVector
        :return:
        """
        for i in range(len(array)):
            color = GREEN if array[i] else RED
            draw_circle(screen, self.__left_location + 2 * i * self.__down_vector, LIGHT_RADIUS, color)

    def __draw_bottom(self, screen, array):
        """

        :param screen:
        :param array:
        :type colors_vector: RoadColorsVector
        :return:
        """
        for i in range(len(array)):
            color = GREEN if array[i] else RED
            draw_circle(screen, self.__bottom_location + 2 * i * self.__right_vector, LIGHT_RADIUS, color)

    def __draw_right(self, screen, array):
        """
        :param screen:
        :param array:
        :type colors_vector: RoadColorsVector
        :return:
        """
        for i in range(len(array)):
            color = GREEN if array[i] else RED
            draw_circle(screen, self.__right_location + 2 * i * self.__top_vector, LIGHT_RADIUS, color)

    def refresh(self, screen, colors_vector):
        """
        Draws all lights
        :param screen:
        :param colors_vector:
        :type colors_vector: RoadColorsVector
        :return:
        """
