from math import sqrt

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __ne__(self, other):
        return not (self == other)
    def __eq__(self, other):
        return self is other or (self.x == other.x and self.y == other.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "Position ({0},{1})".format(self.x, self.y)

    def __getitem__(self, item):
        return self.x if item == 0 else self.y

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

    def copy(self):
        return Position(self.x, self.y)

    def __neg__(self):
        return Position(-self.x, -self.y)


def draw_line(screen, point1: Position, point2: Position, color=BLACK):
    pygame.draw.line(screen, color, [point1.x, point1.y], [point2.x, point2.y])


def draw_car(screen, position: Position, color=BLUE):
    pygame.draw.circle(screen, color, [position.x, position.y], Map.carRadius)


class Road:
    def __init__(self, array):
        self.first = array[0]
        self.second = array[1]

    def __len__(self):
        return 0 if len(self.first) == 0 else len(self.first[0]) * (Map.blockSize + Map.carOffset)

    @property
    def length(self):
        return self.__len__()

    @property
    def width(self):
        return (len(self.first) + len(self.second)) * Map.blockSize

    def get_first_indexes(self):
        for i in range(len(self.first)):
            for q in range(len(self.first[i])):
                yield (i, q)

    def get_second_indexes(self):
        for i in range(len(self.second)):
            for q in range(len(self.second[i])):
                yield (i, q)


# noinspection PyAttributeOutsideInit
class Map:
    blockSize = 15
    minimumOffset = 100
    constOffset = 30
    carRadius = int(blockSize / 2)
    carOffset = int(blockSize * sqrt(2) / 4)

    def __init__(self):
        self.topleft = [50, 50]
        base = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        base_reversed = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.top = Road([[base.copy(), base.copy()], [base_reversed.copy(), base_reversed.copy()]])
        self.bottom = Road([[base.copy()], [base_reversed.copy()]])
        self.left = Road([[base.copy(), base.copy()], [base_reversed.copy(), base_reversed.copy()]])
        self.right = Road([[base.copy(), base.copy(), base.copy()], [base_reversed.copy(), base_reversed.copy()]])
        self.maxYOffset = int(max(self.left.width, self.right.width) / 2)
        self.maxXOffset = int(max(self.top.width, self.bottom.width) / 2)
        self.middle = Position(Map.constOffset + self.left.length + self.maxYOffset,
                               Map.constOffset + self.top.length + self.maxXOffset)
        self.calculate_points()

    def calculate_points(self):

        top_end_left = self.middle - Position(int(self.top.width / 2), self.maxYOffset)
        self.top_start_left = top_end_left - Position(0, self.top.length)
        top_end_right = self.top_start_left + Position(self.top.width, 0)
        self.top_start_right = top_end_right + Position(0, self.top.length)
        self.topPoints = ((self.top_start_left, top_end_left), (self.top_start_right, top_end_right))

        self.left_start_up = self.middle - Position(self.maxXOffset, int(self.left.width / 2))
        left_end_up = self.left_start_up + Position(-self.left.length, 0)
        self.left_start_down = left_end_up + Position(0, self.left.width)
        left_end_down = self.left_start_up + Position(0, self.left.width)
        self.leftPoints = ((self.left_start_up, left_end_up), (self.left_start_down, left_end_down))

        right_end_up = self.middle + Position(self.maxXOffset, -(int(self.right.width / 2)))
        self.right_start_up = right_end_up + Position(self.right.length, 0)
        self.right_start_down = right_end_up + Position(0, self.right.width)
        right_end_down = self.right_start_up + Position(0, self.right.width)
        self.rightPoints = ((self.right_start_up, right_end_up), (self.right_start_down, right_end_down))

        self.down_start_left = self.middle + Position(-int(self.bottom.width / 2), self.maxYOffset)
        down_end_left = self.down_start_left + Position(0, self.bottom.length)
        self.down_start_right = down_end_left + Position(self.bottom.width, 0)
        down_end_right = self.down_start_right - Position(0, self.bottom.length)
        self.downPoints = ((self.down_start_left, down_end_left), (self.down_start_right, down_end_right))

    def seal(self, screen):
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
        self.draw_directions(screen, [self.topPoints, self.rightPoints, self.leftPoints, self.downPoints])
        self.seal(screen)
        self.draw_cars(screen)

    def draw_cars_on_road(self, screen, outsideDir, insideDir, line):
        [draw_car(screen, outsideDir(i, q))
         for (i, q) in line.get_first_indexes() if
         line.first[i][q] != 0]

        [draw_car(screen, insideDir(i, q), RED)
         for (i, q) in line.get_second_indexes() if
         line.second[i][q] != 0]

    def draw_cars(self, screen):
        self.draw_cars_on_road(screen, self.car_top_outside_direction, self.car_top_inside_direction, self.top)
        self.draw_cars_on_road(screen, self.car_left_outside_direction, self.car_left_inside_direction, self.left)
        self.draw_cars_on_road(screen, self.car_right_outside_direction, self.car_right_inside_direction, self.right)
        self.draw_cars_on_road(screen, self.car_down_outside_direction, self.car_down_inside_direction, self.bottom)

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

    @staticmethod
    def car_down_movement_vector(i, q):
        left_offset = Map.carOffset if i == 0 else i * (Map.carOffset + Map.blockSize)
        right_offset = Map.carOffset if q == 0 else q * (Map.carOffset + Map.blockSize)
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
        return 0 if len(direction[0]) == 0 else len(direction[0][0]) * Map.blockSize
