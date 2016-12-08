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


def draw_line(screen, point1: Position, point2: Position, color=BLACK):
    pygame.draw.line(screen, color, [point1.x, point1.y], [point2.x, point2.y])


def draw_car(screen, position: Position, color=BLUE):
    pygame.draw.circle(screen, color, [position.x, position.y], Map.carRadius)


class Road:
    def __init__(self, array):
        self.first = array[0]
        self.second = array[1]

    def __len__(self):
        return 0 if len(self.first) == 0 else len(self.first[0]) * Map.blockSize

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
    carRadius = int(blockSize / 3)

    def __init__(self):
        self.topleft = [50, 50]
        base = [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        base_reversed = [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        multiplier = 1
        self.top = Road([[base * 1] * 2, [base_reversed * 1] * 1])
        self.bottom = Road([[base * 1] * 2, [base_reversed * 1] * 1])
        self.left = Road([[base * 1] * 2, [base_reversed * 1] * 2])
        self.right = Road([[base * 1] * 2, [base_reversed * 1] * 2])
        self.offsetLeft = self.left.length + Map.constOffset
        self.offsetTop = Map.constOffset
        self.offsetMiddle = max(len(self.left.first) * Map.blockSize, len(self.right.first) * Map.blockSize)
        self.calculate_points()

    def calculate_points(self):
        self.top_start_left = Position(self.offsetLeft, self.offsetTop)
        top_end_left = self.top_start_left + Position(0, self.top.length)
        top_start_right = self.top_start_left + Position(self.top.width, 0)
        self.top_end_right = top_start_right + Position(0, self.top.length)
        self.topPoints = ((self.top_start_left, top_end_left), (top_start_right, self.top_end_right))

        self.left_start_up = top_end_left.copy()
        left_end_up = self.left_start_up + Position(-self.left.length, 0)
        left_start_down = self.left_start_up + Position(0, self.left.width)
        self.left_end_down = left_end_up + Position(0, self.left.width)
        self.leftPoints = ((self.left_start_up, left_end_up), (left_start_down, self.left_end_down))

        right_end_up = self.top_end_right.copy()
        self.right_start_up = right_end_up + Position(self.right.length, 0)
        right_start_down = self.right_start_up + Position(0, self.right.width)
        self.right_end_down = right_end_up + Position(0, self.right.width)
        self.rightPoints = ((self.right_start_up, right_end_up), (right_start_down, self.right_end_down))

        self.down_start_left = left_start_down.copy()
        down_end_left = self.down_start_left + Position(0, self.bottom.length)
        down_start_right = self.right_end_down.copy()
        self.down_end_right = down_start_right + Position(0, self.bottom.length)
        self.downPoints = ((self.down_start_left, down_end_left), (down_start_right, self.down_end_right))

    def seal(self, screen):
        directions = []
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

    def draw_cars(self, screen):
        # draw top left
        [draw_car(screen, self.car_top_position1(i, q))
         for (i, q) in self.top.get_first_indexes() if
         self.top.first[i][q] != 0]

        # draw top right
        [draw_car(screen, self.car_top_position2(i, q), RED)
         for (i, q) in self.top.get_second_indexes() if
         self.top.second[i][q] != 0]

        # draw left top
        [draw_car(screen, self.car_left_position1(i, q))
         for (i, q) in self.left.get_first_indexes() if
         self.left.first[i][q] != 0]

        # draw left bottom
        [draw_car(screen, self.car_left_position2(i, q), RED)
         for (i, q) in self.left.get_second_indexes() if
         self.left.second[i][q] != 0]

        # draw right top
        [draw_car(screen, self.car_right_position1(i, q))
         for (i, q) in self.right.get_first_indexes() if
         self.right.first[i][q] != 0]

        # draw right bottom
        [draw_car(screen, self.car_right_position2(i, q), RED)
         for (i, q) in self.right.get_second_indexes() if
         self.right.second[i][q] != 0]

        # draw right top
        [draw_car(screen, self.car_down_position1(i, q))
         for (i, q) in self.bottom.get_first_indexes() if
         self.bottom.first[i][q] != 0]

        # draw right bottom
        [draw_car(screen, self.car_down_position2(i, q), RED)
         for (i, q) in self.bottom.get_second_indexes() if
         self.bottom.second[i][q] != 0]

    def car_top_position1(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.top_end_right - Position(const + i * Map.blockSize, const + q * Map.blockSize)

    def car_top_position2(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.top_start_left + Position(const + i * Map.blockSize, const + q * Map.blockSize)

    def car_left_position1(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.left_start_up - Position(const + q * Map.blockSize, -i * Map.blockSize - const)

    def car_left_position2(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.left_end_down + Position(const + q * Map.blockSize, -i * Map.blockSize - const)

    def car_right_position1(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.right_end_down + Position(const + q * Map.blockSize, -i * Map.blockSize - const)

    def car_right_position2(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.right_start_up - Position(const + q * Map.blockSize, -i * Map.blockSize - const)

    def car_down_position1(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.down_start_left + Position(const + i * Map.blockSize, const + q * Map.blockSize)

    def car_down_position2(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.down_end_right - Position(const + i * Map.blockSize, const + q * Map.blockSize)

    @staticmethod
    def draw_seals(screen, directions):
        for dir in directions:
            draw_line(screen, dir[0], dir[1])

    @staticmethod
    def draw_directions(screen, directions):
        for dir in directions:
            draw_line(screen, dir[0][0], dir[0][1])
            draw_line(screen, dir[1][0], dir[1][1])

    @staticmethod
    def prepare(screen):
        pygame.display.set_caption("Game")
        screen.fill(WHITE)

    @staticmethod
    def get_length(dir):
        return 0 if len(dir[0]) == 0 else len(dir[0][0]) * Map.blockSize
