"""
This module contains class Map and two methods for drawing (line and car)
"""
from collections import namedtuple

import pygame

from Drawing.DataStructures import Position
from Drawing.drawing_consts import *


def draw_line(screen, point1, point2, color=BLACK):
    """
    Draws line between two points on the screen using selected color
    :return: None
    """
    pygame.draw.line(screen, color, [point1.x, point1.y], [point2.x, point2.y])


def draw_car(screen, position, color=BLUE):
    """
    Draws car in selected color and position
    :return: None
    """
    pygame.draw.circle(screen, color, [position.x, position.y], CAR_RADIUS)


PointsPair = namedtuple('PointsPair', ['start', 'end'])
RoadPointsGroup = namedtuple('RoadPointsGroup', ['outside', 'inside'])
MaxOffset = namedtuple('MaxOffset', ['x', 'y'])
PointsQuadruple = namedtuple('PointsQuadruple', ['top', 'left', 'down', 'right'])


class _MapPointsCalculator:
    @staticmethod
    def __calculate_top_points(middle, top, offset):
        top_end_left = middle - Position((top.width * WIDTH_MULTIPLIER) // 2, offset.y)
        top_start_left = top_end_left - Position(0, top.length * LENGTH_MULTIPLIER)
        top_end_right = top_start_left + Position(top.width * WIDTH_MULTIPLIER, 0)
        top_start_right = top_end_right + Position(0, top.length * LENGTH_MULTIPLIER)

        return RoadPointsGroup(PointsPair(top_start_right, top_end_right), PointsPair(top_start_left, top_end_left))

    @staticmethod
    def __calculate_left_points(middle, left, offset):
        left_start_up = middle - Position(offset.x, (left.width * WIDTH_MULTIPLIER) // 2)
        left_end_up = left_start_up + Position(-left.length * LENGTH_MULTIPLIER, 0)
        left_start_down = left_end_up + Position(0, left.width * WIDTH_MULTIPLIER)
        left_end_down = left_start_up + Position(0, left.width * WIDTH_MULTIPLIER)

        return RoadPointsGroup(PointsPair(left_start_up, left_end_up), PointsPair(left_start_down, left_end_down))

    @staticmethod
    def __calculate_down_points(middle, down, offset):
        down_start_left = middle + Position(-(down.width * WIDTH_MULTIPLIER) // 2, offset.y)
        down_end_left = down_start_left + Position(0, down.length * LENGTH_MULTIPLIER)
        down_start_right = down_end_left + Position(down.width * WIDTH_MULTIPLIER, 0)
        down_end_right = down_start_right - Position(0, down.length * LENGTH_MULTIPLIER)

        return RoadPointsGroup(PointsPair(down_start_left, down_end_left), PointsPair(down_start_right, down_end_right))

    @staticmethod
    def __calculate_right_points(middle, right, offset):
        right_end_up = middle + Position(offset.x, -(right.width * WIDTH_MULTIPLIER) // 2)
        right_start_up = right_end_up + Position(right.length * LENGTH_MULTIPLIER, 0)
        right_start_down = right_end_up + Position(0, right.width * WIDTH_MULTIPLIER)
        right_end_down = right_start_up + Position(0, right.width * WIDTH_MULTIPLIER)

        return RoadPointsGroup(PointsPair(right_start_down, right_end_down), PointsPair(right_start_up, right_end_up))

    @staticmethod
    def calculate_points(middle, roads, offset):
        """
        :rtype: PointsQuadruple
        """
        top_points = _MapPointsCalculator.__calculate_top_points(middle, roads["top"], offset)
        left_points = _MapPointsCalculator.__calculate_left_points(middle, roads["left"], offset)
        down_points = _MapPointsCalculator.__calculate_down_points(middle, roads["down"], offset)
        right_points = _MapPointsCalculator.__calculate_right_points(middle, roads["right"], offset)
        return PointsQuadruple(top_points, left_points, down_points, right_points)


class _MapVectorsCalculator:
    def __init__(self, points):
        self.__points = points

    def car_top_outside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.top.outside.start + _MapVectorsCalculator.up_movement_vector(i, q)

    def car_down_outside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.down.outside.start + _MapVectorsCalculator.down_movement_vector(i, q)

    def car_left_outside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.left.outside.start + _MapVectorsCalculator.left_movement_vector(i, q)

    def car_right_outside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.right.outside.start + _MapVectorsCalculator.right_movement_vector(i, q)

    def car_top_inside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.top.inside.start + _MapVectorsCalculator.down_movement_vector(i, q)

    def car_down_inside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.down.inside.start + _MapVectorsCalculator.up_movement_vector(i, q)

    def car_left_inside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.left.inside.start + _MapVectorsCalculator.right_movement_vector(i, q)

    def car_right_inside_direction(self, i, q):
        """
        :param i: int
        :param q: int
        :rtype: Position
        """
        return self.__points.right.inside.start + _MapVectorsCalculator.left_movement_vector(i, q)

    @staticmethod
    def down_movement_vector(i, j):
        left_offset = CAR_OFFSET + CAR_RADIUS + i * LENGTH_MULTIPLIER
        right_offset = CAR_OFFSET + CAR_RADIUS + j * WIDTH_MULTIPLIER
        return Position(left_offset, right_offset)

    @staticmethod
    def up_movement_vector(i, q):
        return - _MapVectorsCalculator.down_movement_vector(i, q)

    @staticmethod
    def left_movement_vector(i, q):
        p = _MapVectorsCalculator.down_movement_vector(q, i)
        return Position(-p.x, p.y)

    @staticmethod
    def right_movement_vector(i, q):
        return -_MapVectorsCalculator.left_movement_vector(i, q)


# noinspection PyAttributeOutsideInit
class Map:
    """
    Map class, used to draw crossroads
    """

    def __init__(self, vectors, roads):
        self.roads = roads
        self.board = self.__generate_board(vectors)
        self.__offset = MaxOffset(
            int(max(self.top.width * WIDTH_MULTIPLIER, self.bottom.width * WIDTH_MULTIPLIER) / 2),
            int(max(self.left.width * WIDTH_MULTIPLIER, self.right.width * WIDTH_MULTIPLIER) / 2))
        self.__middle = Position(CONST_OFFSET + self.left.length * LENGTH_MULTIPLIER + self.__offset.y,
                                 CONST_OFFSET + self.top.length * LENGTH_MULTIPLIER + self.__offset.x)
        self.points = _MapPointsCalculator.calculate_points(self.__middle, self.roads, self.__offset)
        """:type : PointsQuadruple"""
        self._vector_calculator = _MapVectorsCalculator(self.points)

    def draw(self, screen):
        """
        Draws whole state
        :param screen:
        :return:
        """
        self.draw_directions(screen, [self.points.top, self.points.right, self.points.left, self.points.down])
        self.__seal(screen)
        self.__draw_cars(screen)

    def __seal(self, screen):
        """
        Draws intervals between every two adjacent roads.
        """
        directions = []
        # sealing when road is empty
        if self.left.length <= 0:
            directions.append([self.points.left[0][0], self.points.left[1][0]])
        if self.right.length <= 0:
            directions.append(
                [self.points.right[0][0], self.points.right[1][0]])
        if self.top.length <= 0:
            directions.append([self.points.top[0][0], self.points.top[1][0]])
        if self.bottom.length <= 0:
            directions.append([self.points.down[0][0], self.points.down[1][0]])
        self.draw_seals(screen, directions)

    def __draw_cars(self, screen):
        Map.__draw_cars_on_road(screen,
                                self._vector_calculator.car_top_outside_direction,
                                self._vector_calculator.car_top_inside_direction, self.top)
        Map.__draw_cars_on_road(screen,
                                self._vector_calculator.car_left_outside_direction,
                                self._vector_calculator.car_left_inside_direction, self.left)
        Map.__draw_cars_on_road(screen,
                                self._vector_calculator.car_right_outside_direction,
                                self._vector_calculator.car_right_inside_direction, self.right)
        Map.__draw_cars_on_road(screen,
                                self._vector_calculator.car_down_outside_direction,
                                self._vector_calculator.car_down_inside_direction, self.bottom)
        self.__draw_cars_on_board(screen,
                                  self.points.left.outside.start
                                  )

    @property
    def top(self):
        return self.roads["top"]

    @top.setter
    def top(self, data):
        self.roads["top"] = data

    @property
    def right(self):
        return self.roads["right"]

    @right.setter
    def right(self, data):
        self.roads["right"] = data

    @property
    def left(self):
        return self.roads["left"]

    @left.setter
    def left(self, data):
        self.roads["left"] = data

    @property
    def bottom(self):
        return self.roads["down"]

    @bottom.setter
    def bottom(self, data):
        self.roads["down"] = data

    @staticmethod
    def draw_seals(screen, directions):
        for direction in directions:
            draw_line(screen, direction[0], direction[1])

    @staticmethod
    def __generate_board(roads_vectors):
        """
        :type roads_vectors : List[RoadSizeVector]
        :return: returns list for middle part of crossroad
        :rtype List[[int]]
        """
        left_right_max = max(roads_vectors[1].out_lanes_count + roads_vectors[1].in_lanes_count,
                             roads_vectors[3].out_lanes_count + roads_vectors[3].in_lanes_count,
                             )
        top_down_max = max(roads_vectors[0].out_lanes_count + roads_vectors[0].in_lanes_count,
                           roads_vectors[2].out_lanes_count + roads_vectors[2].in_lanes_count,
                           )
        return [
                   [0] * top_down_max
               ] * left_right_max

    @staticmethod
    def draw_directions(screen, directions):
        for direction in directions:
            draw_line(screen, direction[0][0], direction[0][1])
            draw_line(screen, direction[1][0], direction[1][1])

    @staticmethod
    def prepare(screen):
        pygame.display.set_caption("Game")
        screen.fill(WHITE)

    def __draw_cars_on_board(self, screen, start_point):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] is not None and self.board[i][j] != 0:
                    draw_car(screen, start_point +
                             _MapVectorsCalculator.down_movement_vector(j, i)
                             )

    @staticmethod
    def __draw_cars_on_road(screen, outside_dir, inside_dir, line):
        for (i, q) in line.out_indexes:
            if line.out_lanes[i][q] is not None and line.out_lanes[i][q] != 0:
                draw_car(screen, outside_dir(i, q))
        for (i, q) in line.in_indexes:
            if line.in_lanes[i][q] is not None and line.in_lanes[i][q] != 0:
                draw_car(screen, inside_dir(i, q), RED)
