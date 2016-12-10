"""
This module contains class Map and two methods for drawing (line and car)
"""
from Drawing.DataStructures import Position, Road, RoadSizeVector
from Drawing.DataStructures import get_empty_road
from Drawing.drawing_consts import *
import pygame


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


# noinspection PyAttributeOutsideInit
class Map:
    """
    Map class, used to draw crossroads
    """
    defaultVectors = [
        RoadSizeVector(12, 2, 2),  # top
        RoadSizeVector(12, 2, 2),  # left
        RoadSizeVector(12, 2, 2),  # bottom
        RoadSizeVector(12, 2, 2),  # right
    ]

    def __init__(self, vectors=defaultVectors):
        self.topleft = [50, 50]
        self.roads = {
            "top": get_empty_road(vectors[0]),
            "bottom": get_empty_road(vectors[1]),
            "left": get_empty_road(vectors[2]),
            "right": get_empty_road(vectors[3])
        }
        self.max_y_offset = int(max(self.left.width, self.right.width) / 2)
        self.max_x_offset = int(max(self.top.width, self.bottom.width) / 2)
        self.middle = Position(
            CONST_OFFSET + self.left.length + self.max_y_offset,
            CONST_OFFSET + self.top.length + self.max_x_offset)
        self.calculate_points()

    def calculate_points(self):

        top_end_left = self.middle - Position(int(self.top.width / 2),
                                              self.max_y_offset)
        self.top_start_left = top_end_left - Position(0, self.top.length)
        top_end_right = self.top_start_left + Position(self.top.width, 0)
        self.top_start_right = top_end_right + Position(0, self.top.length)
        self.topPoints = ((self.top_start_left, top_end_left),
                          (self.top_start_right, top_end_right))

        self.left_start_up = self.middle - Position(self.max_x_offset,
                                                    int(self.left.width / 2))
        left_end_up = self.left_start_up + Position(-self.left.length, 0)
        self.left_start_down = left_end_up + Position(0, self.left.width)
        left_end_down = self.left_start_up + Position(0, self.left.width)
        self.leftPoints = ((self.left_start_up, left_end_up),
                           (self.left_start_down, left_end_down))

        right_end_up = self.middle + Position(self.max_x_offset,
                                              -(int(self.right.width / 2)))
        self.right_start_up = right_end_up + Position(self.right.length, 0)
        self.right_start_down = right_end_up + Position(0, self.right.width)
        right_end_down = self.right_start_up + Position(0, self.right.width)
        self.rightPoints = ((self.right_start_up, right_end_up),
                            (self.right_start_down, right_end_down))

        self.down_start_left = self.middle + Position(
            -int(self.bottom.width / 2), self.max_y_offset)
        down_end_left = self.down_start_left + Position(0, self.bottom.length)
        self.down_start_right = down_end_left + Position(self.bottom.width, 0)
        down_end_right = self.down_start_right - Position(0,
                                                          self.bottom.length)
        self.downPoints = ((self.down_start_left, down_end_left),
                           (self.down_start_right, down_end_right))

    def seal(self, screen):
        """
        Draws intervals between every two adjacent roads.
        """
        directions = []
        # sealing when road is empty
        if self.left.length <= 0:
            directions.append([self.leftPoints[0][0], self.leftPoints[1][0]])
        if self.right.length <= 0:
            directions.append([self.rightPoints[0][0], self.rightPoints[1][0]])
        if self.top.length <= 0:
            directions.append([self.topPoints[0][0], self.topPoints[1][0]])
        if self.bottom.length <= 0:
            directions.append([self.downPoints[0][0], self.downPoints[1][0]])
        self.draw_seals(screen, directions)

    def draw(self, screen):
        self.draw_directions(screen, [self.topPoints, self.rightPoints,
                                      self.leftPoints, self.downPoints])
        self.seal(screen)
        self.draw_cars(screen)

    def draw_cars_on_road(self, screen, outside_dir, inside_dir, line):
        [draw_car(screen, outside_dir(i, q))
         for (i, q) in line.get_first_indexes() if
         line.first[i][q] != 0]

        [draw_car(screen, inside_dir(i, q), RED)
         for (i, q) in line.get_second_indexes() if
         line.second[i][q] != 0]

    def draw_cars(self, screen):
        self.draw_cars_on_road(screen, self.car_top_outside_direction,
                               self.car_top_inside_direction, self.top)
        self.draw_cars_on_road(screen, self.car_left_outside_direction,
                               self.car_left_inside_direction, self.left)
        self.draw_cars_on_road(screen, self.car_right_outside_direction,
                               self.car_right_inside_direction, self.right)
        self.draw_cars_on_road(screen, self.car_down_outside_direction,
                               self.car_down_inside_direction, self.bottom)

    def car_top_outside_direction(self, i: int, q: int):
        return self.top_start_right + Map.car_up_movement_vector(i, q)

    def car_down_outside_direction(self, i: int, q: int):
        return self.down_start_left + Map.car_down_movement_vector(i, q)

    def car_left_outside_direction(self, i: int, q: int):
        return self.left_start_up + Map.car_left_movement_vector(i, q)

    def car_right_outside_direction(self, i: int, q: int):
        return self.right_start_down + Map.car_right_movement_vector(i, q)

    def car_top_inside_direction(self, i: int, q: int):
        return self.top_start_left + Map.car_down_movement_vector(i, q)

    def car_down_inside_direction(self, i: int, q: int):
        return self.down_start_right + Map.car_up_movement_vector(i, q)

    def car_left_inside_direction(self, i: int, q: int):
        return self.left_start_down + Map.car_right_movement_vector(i, q)

    def car_right_inside_direction(self, i: int, q: int):
        return self.right_start_up + Map.car_left_movement_vector(i, q)

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
    def car_down_movement_vector(i, q):
        left_offset = CAR_OFFSET if i == 0 else i * (CAR_OFFSET + BLOCK_SIZE)
        right_offset = CAR_OFFSET if q == 0 else q * (CAR_OFFSET + BLOCK_SIZE)
        return Position(left_offset, right_offset)

    @staticmethod
    def car_up_movement_vector(i, q):
        return - Map.car_down_movement_vector(i, q)

    @staticmethod
    def car_left_movement_vector(i, q):
        p = Map.car_down_movement_vector(q, i)
        return Position(-p.x, p.y)

    @staticmethod
    def car_right_movement_vector(i, q):
        return -Map.car_left_movement_vector(i, q)

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
        return 0 if len(direction[0]) == 0 else len(
            direction[0][0]) * BLOCK_SIZE
