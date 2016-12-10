"""
This module contains class Map and two methods for drawing (line and car)
"""
from collections import namedtuple

import pygame

from Drawing.DataStructures import Position, RoadSizeVector
from Drawing.DataStructures import get_empty_road
from Drawing.drawing_consts import *


def draw_line(screen, point1: Position, point2: Position, color=BLACK):
    """
    Draws line between two points on the screen using selected color
    :return: None
    """
    pygame.draw.line(screen, color, [point1.x, point1.y], [point2.x, point2.y])


def draw_car(screen, position: Position, color=BLUE):
    """
    Draws car in selected color and position
    :return: None
    """
    pygame.draw.circle(screen, color, [position.x, position.y], CAR_RADIUS)


PointsPair = namedtuple('PointsPair', ['start', 'end'])
RoadPointsGroup = namedtuple('RoadPointsGroup', ['outside', 'inside'])
MaxOffset = namedtuple('MaxOffset', ['x', 'y'])
PointsQuadruple = namedtuple('PointsQuadruple', ['top', 'left', 'down', 'right'])


# noinspection PyAttributeOutsideInit
class Map:
    """
    Map class, used to draw crossroads
    """
    defaultVectors = [
        RoadSizeVector(5, 2, 2),  # top
        RoadSizeVector(5, 2, 2),  # left
        RoadSizeVector(5, 2, 2),  # bottom
        RoadSizeVector(5, 2, 2)  # right
    ]

    def __init__(self, vectors=defaultVectors):
        self.roads = {
            "top": get_empty_road(vectors[0]),
            "bottom": get_empty_road(vectors[2]),
            "left": get_empty_road(vectors[1]),
            "right": get_empty_road(vectors[3])
        }
        self.offset = MaxOffset(
            int(max(self.top.width * BLOCK_SIZE, self.bottom.width * BLOCK_SIZE) / 2),
            int(max(self.left.width * BLOCK_SIZE, self.right.width * BLOCK_SIZE) / 2))
        self.middle = Position(CONST_OFFSET + self.left.length * LENGTH_MULTIPLIER + self.offset.y,
                               CONST_OFFSET + self.top.length * LENGTH_MULTIPLIER + self.offset.x)
        self.calculate_points()

    def calculate_top_points(self):
        multiplier = LENGTH_MULTIPLIER
        top_end_left = self.middle - Position(int(self.top.width / 2) * BLOCK_SIZE, self.offset.y)
        top_start_left = top_end_left - Position(0, self.top.length * multiplier)
        top_end_right = top_start_left + Position(self.top.width * BLOCK_SIZE, 0)
        top_start_right = top_end_right + Position(0, self.top.length * multiplier)
        return RoadPointsGroup(PointsPair(top_start_right, top_end_right), PointsPair(top_start_left, top_end_left))

    def calculate_left_points(self):
        mpl = LENGTH_MULTIPLIER
        left_start_up = self.middle - Position(self.offset.x, int(self.left.width / 2) * BLOCK_SIZE)
        left_end_up = left_start_up + Position(-self.left.length * mpl, 0)
        left_start_down = left_end_up + Position(0, self.left.width * BLOCK_SIZE)
        left_end_down = left_start_up + Position(0, self.left.width * BLOCK_SIZE)
        return RoadPointsGroup(PointsPair(left_start_up, left_end_up), PointsPair(left_start_down, left_end_down))

    def calculate_down_points(self):
        multiplier = LENGTH_MULTIPLIER
        down_start_left = self.middle + Position(-int(self.bottom.width / 2) * BLOCK_SIZE, self.offset.y)
        down_end_left = down_start_left + Position(0, self.bottom.length * multiplier)
        down_start_right = down_end_left + Position(self.bottom.width * BLOCK_SIZE, 0)
        down_end_right = down_start_right - Position(0, self.bottom.length * multiplier)

        return RoadPointsGroup(
            PointsPair(down_start_left, down_end_left),
            PointsPair(down_start_right, down_end_right))

    def calculate_right_points(self):
        multiplier = LENGTH_MULTIPLIER
        right_end_up = self.middle + Position(self.offset.x, -(int(self.right.width / 2) * BLOCK_SIZE))
        right_start_up = right_end_up + Position(self.right.length * multiplier, 0)
        right_start_down = right_end_up + Position(0, self.right.width * BLOCK_SIZE)
        right_end_down = right_start_up + Position(0, self.right.width * BLOCK_SIZE)
        return RoadPointsGroup(PointsPair(right_start_down, right_end_down), PointsPair(right_start_up, right_end_up))

    def calculate_points(self):
        top_points = self.calculate_top_points()
        left_points = self.calculate_left_points()
        down_points = self.calculate_down_points()
        right_points = self.calculate_right_points()
        self.points = PointsQuadruple(top_points, left_points, down_points, right_points)

    def seal(self, screen):
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

    def draw(self, screen):
        self.draw_directions(screen, [self.points.top, self.points.right, self.points.left, self.points.down])
        self.seal(screen)
        self.draw_cars(screen)

    @staticmethod
    def draw_cars_on_road(screen, outside_dir, inside_dir, line):
        for (i, q) in line.get_first_indexes():
            if line.first[i][q] != 0:
                draw_car(screen, outside_dir(i, q))
        for (i, q) in line.get_second_indexes():
            if line.second[i][q] != 0:
                draw_car(screen, inside_dir(i, q), RED)

    def draw_cars(self, screen):
        self.draw_cars_on_road(screen, self.car_top_outside_direction, self.car_top_inside_direction, self.top)
        self.draw_cars_on_road(screen, self.car_left_outside_direction, self.car_left_inside_direction, self.left)
        self.draw_cars_on_road(screen, self.car_right_outside_direction, self.car_right_inside_direction, self.right)
        self.draw_cars_on_road(screen, self.car_down_outside_direction, self.car_down_inside_direction, self.bottom)

    def car_top_outside_direction(self, i: int, q: int):
        return self.points.top.outside.start + Map.up_movement_vector(i, q)

    def car_down_outside_direction(self, i: int, q: int):
        return self.points.down.outside.start + Map.down_movement_vector(i, q)

    def car_left_outside_direction(self, i: int, q: int):
        return self.points.left.outside.start + Map.left_movement_vector(i, q)

    def car_right_outside_direction(self, i: int, q: int):
        return self.points.right.outside.start + Map.right_movement_vector(i,
                                                                           q)

    def car_top_inside_direction(self, i: int, q: int):
        return self.points.top.inside.start + Map.down_movement_vector(i, q)

    def car_down_inside_direction(self, i: int, q: int):
        return self.points.down.inside.start + Map.up_movement_vector(i, q)

    def car_left_inside_direction(self, i: int, q: int):
        return self.points.left.inside.start + Map.right_movement_vector(i, q)

    def car_right_inside_direction(self, i: int, q: int):
        return self.points.right.inside.start + Map.left_movement_vector(i, q)

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
        return self.roads["bottom"]

    @bottom.setter
    def bottom(self, data):
        self.roads["bottom"] = data

    @staticmethod
    def down_movement_vector(i, q):
        left_offset = CAR_OFFSET if i == 0 else i * (CAR_OFFSET + BLOCK_SIZE)
        right_offset = CAR_OFFSET if q == 0 else q * (CAR_OFFSET + BLOCK_SIZE)
        return Position(left_offset, right_offset)

    @staticmethod
    def up_movement_vector(i, q):
        return - Map.down_movement_vector(i, q)

    @staticmethod
    def left_movement_vector(i, q):
        p = Map.down_movement_vector(q, i)
        return Position(-p.x, p.y)

    @staticmethod
    def right_movement_vector(i, q):
        return -Map.left_movement_vector(i, q)

    @staticmethod
    def draw_seals(screen, directions):
        for direction in directions:
            draw_line(screen, direction[0], direction[1])

    @staticmethod
    def draw_directions(screen, directions):
        for direction in directions:
            draw_line(screen, direction[0][0], direction[0][1])
            draw_line(screen, direction[1][0], direction[1][1])

    @staticmethod
    def prepare(screen):
        pygame.display.set_caption("Game")
        screen.fill(WHITE)

    @staticmethod
    def get_length(direction):
        return 0 if len(direction[0]) == 0 else len(direction[0][0]) * BLOCK_SIZE
