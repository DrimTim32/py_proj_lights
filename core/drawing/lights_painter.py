from core.data_structures.vector import Vector
from core.drawing.drawing_consts import LIGHT_OFFSET, LIGHT_RADIUS
from core.drawing.drawing_helpers import draw_circle
from core.drawing.drawing_consts import GREEN, RED
from collections import namedtuple

"""Structure for lists of colors"""
RoadSizeVector = namedtuple('ColorsVector', ['top', 'left', 'bottom', 'right'])


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

    def draw_empty(self, screen):
        self.__draw_top(screen)
        self.__draw_left(screen)
        self.__draw_bottom(screen)
        self.__draw_right(screen)

    def __draw_top(self, screen, array=[GREEN]):
        """

        :param screen:
        :param array:
        :type array: list[tuple[tuple(int,int,int),int]]
        :return:
        """
        draw_circle(screen, self.__top_location, LIGHT_RADIUS)

    def __draw_left(self, screen, array=[GREEN, RED, GREEN]):
        """

        :param screen:
        :param array:
        :type array: list[tuple[tuple(int,int,int),int]]
        :return:
        """
        curr_location = self.__left_location.copy()
        for color in array:
            draw_circle(screen, curr_location, LIGHT_RADIUS, color)
            curr_location += self.__down_vector * 2

    def __draw_bottom(self, screen, array=[GREEN, GREEN]):
        """

        :param screen:
        :param array:
        :type array: list[tuple[tuple(int,int,int),int]]
        :return:
        """
        curr_location = self.__bottom_location.copy()
        for color in array:
            draw_circle(screen, curr_location, LIGHT_RADIUS, color)
            curr_location += self.__right_vector * 2

    def __draw_right(self, screen, array=[GREEN]):
        """

        :param screen:
        :param array:
        :type array: list[tuple[tuple(int,int,int),int]]
        :return:
        """
        draw_circle(screen, self.__right_location, LIGHT_RADIUS)

    def refresh(self, screen, colors_vector):
        """
        Draws all lights
        :param screen:
        :param colors_vector:
        :type colors_vector: RoadSizeVector
        :return:
        """
