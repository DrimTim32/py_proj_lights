import pygame
from math import sqrt

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


def draw_car(screen, position: Position):
    pygame.draw.circle(screen, BLUE, [position.x, position.y], Map.carRadius)


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


# noinspection PyAttributeOutsideInit
class Map:
    blockSize = 15
    minimumOffset = 100
    constOffset = 30
    carRadius = int(blockSize / 3)

    def __init__(self):
        self.topleft = [50, 50]
        self.top = Road([[[1] * 10] * 3, [[1] * 10] * 1])
        self.left = Road([[[1] * 10] * 1, [[1] * 10] * 1])
        self.down = Road([[[1] * 10] * 0, [[1] * 10] * 0])
        self.right = Road([[[1] * 10] * 1, [[1] * 10] * 1])
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

        left_start_up = top_end_left.copy()
        left_end_up = left_start_up + Position(-self.left.length, 0)
        left_start_down = left_start_up + Position(0, self.left.width)
        left_end_down = left_end_up + Position(0, self.left.width)
        self.leftPoints = ((left_start_up, left_end_up), (left_start_down, left_end_down))

        right_start_up = self.top_end_right.copy()
        right_end_up = right_start_up + Position(self.right.length, 0)
        right_start_down = right_start_up + Position(0, self.right.width)
        right_end_down = right_end_up + Position(0, self.right.width)
        self.rightPoints = ((right_start_up, right_end_up), (right_start_down, right_end_down))

        down_start_left = left_start_down.copy()
        down_end_left = down_start_left + Position(0, self.down.length)
        down_start_right = right_start_down.copy()
        down_end_right = down_start_right + Position(0, self.down.length)
        self.downPoints = ((down_start_left, down_end_left), (down_start_right, down_end_right))

    def seal(self, screen):
        directions = []
        if self.left.length <= 0:
            directions.append([self.leftPoints[0][0], self.leftPoints[1][0]])
        if self.right.length <= 0:
            directions.append([self.rightPoints[0][0], self.rightPoints[1][0]])
        if self.top.length <= 0:
            directions.append([self.topPoints[0][0], self.topPoints[1][0]])
        if self.down.length <= 0:
            directions.append([self.downPoints[0][0], self.downPoints[1][0]])
        self.draw_seals(screen, directions)

    def draw(self, screen):
        self.draw_directions(screen, [self.topPoints, self.rightPoints, self.leftPoints, self.downPoints])
        self.seal(screen)
        self.draw_cars(screen)

    def draw_cars(self, screen):
        # draw top left
        for i in range(len(self.top.first)):
            for q in range(len(self.top.first[i])):
                if self.top.first[i][q] != 0:
                    draw_car(screen, self.car_top_position(i, q))
        # draw top right
        for i in range(len(self.top.second)):
            for q in range(len(self.top.second[i])):
                if self.top.second[i][q] != 0:
                    draw_car(screen, self.car_top_position2(i, q))
        # draw left top
        for i in range(len(self.left.first)):
            for q in range(len(self.left.first[i])):
                if self.left.first[i][q] != 0:
                    pass

    def car_top_position(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.top_start_left + Position(const + i * Map.blockSize, const + q * Map.blockSize)

    def car_top_position2(self, i: int, q: int):
        const = int(Map.blockSize * sqrt(2) / 3)
        return self.top_end_right - Position(const + i * Map.blockSize, const + q * Map.blockSize)

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
