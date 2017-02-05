"""This file contains LightsPainter class and helper functions"""
from core.data_structures.vector import Vector
from core.data_structures.points_structures import PointsQuadruple
from core.drawing.drawing_consts import LIGHT_OFFSET, LIGHT_RADIUS
from core.drawing.drawing_helpers import draw_circle
from core.drawing.drawing_consts import GREEN, RED
from core.data_structures.enums import Directions


def _draw_light(screen, position, color):
    """
    Draws light on the screen
    :param screen: screen to draw on
    :param position: light position
    :param color: light color
    :return: None
    """
    draw_circle(screen, position, LIGHT_RADIUS, color)


def _draw_lights(screen, start_point, move_vector, colors_array):
    """
    Draws set of lights distanced by  2 * move_vector
    :param screen: screen to draw on
    :param start_point: first light position
    :param move_vector: distance vector
    :param colors_array: color list
    :return:
    """
    for index, color in enumerate(colors_array):
        _draw_light(screen, start_point + 2 * index * move_vector, color)


class LightsPainter:
    """Class used to draw lights on screen"""

    def __init__(self, top_location, left_location, bottom_location, right_location):
        """
        Inits whole painter
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

        top_location = top_location + self.__top_vector + self.__left_vector
        left_location = left_location + self.__down_vector + self.__left_vector
        bottom_location = bottom_location + self.__down_vector + self.__right_vector
        right_location = right_location + self.__top_vector + self.__right_vector

        self.__locations = PointsQuadruple(top_location, left_location, bottom_location, right_location)

    def draw(self, screen, lights_dict):
        """
        Draws lights on the screen
        :param screen:
        :param lights_dict:
        :return:
        """
        for direction, lights in lights_dict.items():
            self.__draw(screen, direction, lights)

    def __draw(self, screen, direction, light_colors):
        """
        Draws lights on the screen depending of road direction
        :param screen: screen to draw
        :param direction: road direction
        :param light_colors: light colors list
        :type direction: Directions
        :type light_colors: list[tuple(int,int,int)]
        :return:
        """
        light_colors = [GREEN if q else RED for q in light_colors[::-1]]
        if direction == Directions.BOTTOM:
            self.__draw_bottom(screen, light_colors)
        if direction == Directions.TOP:
            self.__draw_top(screen, light_colors)
        if direction == Directions.RIGHT:
            self.__draw_right(screen, light_colors)
        if direction == Directions.LEFT:
            self.__draw_left(screen, light_colors)

    def __draw_top(self, screen, colors_array):
        """
        :param screen:
        :param colors_array:
        :type colors_vector: list[tuple(int,int,int)]
        :return:
        """
        _draw_lights(screen, self.__locations.top, self.__left_vector, colors_array)

    def __draw_left(self, screen, colors_array):
        """
        :param screen:
        :param colors_array:
        :type colors_vector: list[tuple(int,int,int)]
        :return:
        """
        _draw_lights(screen, self.__locations.left, self.__down_vector, colors_array)

    def __draw_bottom(self, screen, colors_array):
        """

        :param screen:
        :param colors_array:
        :type colors_vector: list[tuple(int,int,int)]
        :return:
        """
        _draw_lights(screen, self.__locations.down, self.__right_vector, colors_array)

    def __draw_right(self, screen, colors_array):
        """
        :param screen:
        :param colors_array:
        :type colors_vector: list[tuple(int,int,int)]
        :return:
        """
        _draw_lights(screen, self.__locations.right, self.__top_vector, colors_array)
