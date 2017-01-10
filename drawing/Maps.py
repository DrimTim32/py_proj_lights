"""
This module contains class Map and two methods for drawing (line and car)
"""
from collections import namedtuple

import pygame

from Drawing.drawing_consts import *
from core.DataStructures import Position


# region drawing funcitons
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


# endregion

# region named tuples
PointsPair = namedtuple('PointsPair', ['start', 'end'])
RoadPointsGroup = namedtuple('RoadPointsGroup', ['outside', 'inside'])
MaxOffset = namedtuple('MaxOffset', ['x', 'y'])
PointsQuadruple = namedtuple('PointsQuadruple', ['top', 'left', 'down', 'right'])


# endregion

# region calculating classes
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
        down_points = _MapPointsCalculator.__calculate_down_points(middle, roads["bottom"], offset)
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


# endregion

def create_map_painter(intersection, roads):
    """
    Map painter initializer
    :param intersection: Intersection data, such as road lengths
    :type intersection: Intersection
    :param roads: Road definitions top,left,right,bottom
    :type roads: dict[str,RoadSizeVector]
    """

    board = intersection.array

    __offset = MaxOffset(
        int(max(roads["top"].width * WIDTH_MULTIPLIER, roads["bottom"].width * WIDTH_MULTIPLIER) / 2),
        int(max(roads["left"].width * WIDTH_MULTIPLIER, roads["right"].width * WIDTH_MULTIPLIER) / 2))
    """:type : MaxOffset"""
    __middle = Position(CONST_OFFSET + roads["left"].length * LENGTH_MULTIPLIER + __offset.y,
                        CONST_OFFSET + roads["top"].length * LENGTH_MULTIPLIER + __offset.x)
    """:type: Position"""


    points = _MapPointsCalculator.calculate_points(__middle, roads, __offset)
    """:type : PointsQuadruple"""

    _vector_calculator = _MapVectorsCalculator(points)
    """:type : _MapVectorsCalculator"""

    return MapPainter(points.left.outside.start, board, _vector_calculator, points)


class MapPainter:
    """
    Draws map
    """

    def __init__(self, board_start_point, board, vectors_calculator, points):
        """

        :param board_start_point:
        :param board:
        :param vectors_calculator:
        :param points:
        """
        self.board_start_point = board_start_point
        self.board = board
        self._vector_calculator = vectors_calculator
        self.border_points = points


    def draw(self, screen, roads):
        """
        Draws whole state
        :param screen:
        :param roads:

        :type points: list[Road]
        :return:
        """
        screen.fill(WHITE)  # TODO : remove

        top, left, down, right = self.border_points
        self.__draw_borders(screen, [top, left, down, right])
        self.__seal(screen, roads, [top, left, down, right])
        self.__draw_cars(screen, roads)

    def __seal(self, screen, roads, points):
        """
        Draws intervals between every two adjacent roads.
        :param roads:
        :type points: list[Road]
        """
        top_road, left_road, bottom_road, right_road = roads

        top, left, bottom, right = points
        directions = []
        # region empty roads ifs
        # sealing when road is empty

        if left_road.length <= 0:
            directions.append([left[0][0], left[1][0]])
        if right_road.length <= 0:
            directions.append([top[0][0], bottom[1][1]])
        if top_road.length <= 0:
            directions.append([top[0][0], top[1][0]])
        if bottom_road.length <= 0:
            directions.append([bottom[0][0], bottom[1][0]])
        # endregion

        self.__draw_seals(screen, directions)

    def __draw_cars(self, screen, points):

        """
        Draws cars on the screen
        :param screen:
        :return:
        """
        top, left, bottom, right = points
        self.__draw_cars_on_road(screen,
                                 self._vector_calculator.car_top_outside_direction,
                                 self._vector_calculator.car_top_inside_direction, top)
        self.__draw_cars_on_road(screen,
                                 self._vector_calculator.car_left_outside_direction,
                                 self._vector_calculator.car_left_inside_direction, left)
        self.__draw_cars_on_road(screen,
                                 self._vector_calculator.car_right_outside_direction,
                                 self._vector_calculator.car_right_inside_direction, right)
        self.__draw_cars_on_road(screen,
                                 self._vector_calculator.car_down_outside_direction,
                                 self._vector_calculator.car_down_inside_direction, bottom)
        self.__draw_cars_on_board(self.board, screen, self.board_start_point)


    @staticmethod
    def __draw_cars_on_board(board, screen, start_point):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] is not None and board[i][j] != 0:
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

    @staticmethod
    def __draw_seals(screen, directions):
        for direction in directions:
            draw_line(screen, direction[0], direction[1])

    @staticmethod
    def __draw_borders(screen, directions):
        for direction in directions:
            draw_line(screen, direction[0][0], direction[0][1])
            draw_line(screen, direction[1][0], direction[1][1])

    @staticmethod
    def prepare(screen):
        pygame.display.set_caption("Simulation")
        screen.fill(WHITE)
