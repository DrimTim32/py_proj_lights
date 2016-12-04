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

    def copy(self):
        return Position(self.x, self.y)


def draw_line(screen, point1: Position, point2: Position, color=BLACK):
    pygame.draw.line(screen, color, [point1.x, point1.y], [point2.x, point2.y])


class Map:
    blockSize = 20
    minimumOffset = 100

    def __init__(self):
        self.topleft = [50, 50]
        self.top = [[[0] * 0], [[0] * 0]]
        self.left = [[[0] * 0], [[0] * 0]]
        self.down = [[[0] * 0], [[0] * 0]]
        self.right = [[[0] * 0], [[0] * 0]]
        self.offsetLeft = max(len(self.left[0]) * Map.blockSize, Map.minimumOffset)
        self.offsetTop = max(len(self.top[0]) * Map.blockSize, Map.minimumOffset)
        self.offsetMiddle = max(len(self.left[0]) * Map.blockSize, len(self.right[0]) * Map.blockSize)
        self.calculatePoints()

    @property
    def left_road_length(self):
        return len(self.left[0][0]) * Map.blockSize

    @property
    def top_road_length(self):
        return len(self.top[0][0]) * Map.blockSize

    @property
    def right_road_length(self):
        return len(self.right[0][0]) * Map.blockSize

    @property
    def down_road_length(self):
        return len(self.down[0][0]) * Map.blockSize

    @property
    def left_road_width(self):
        return (len(self.left[0]) + len(self.left[1])) * Map.blockSize

    @property
    def top_road_width(self):
        return (len(self.top[0]) + len(self.top[1])) * Map.blockSize

    @property
    def right_road_width(self):
        return (len(self.right[0]) + len(self.right[1])) * Map.blockSize

    @property
    def down_road_width(self):
        return (len(self.down[0]) + len(self.down[1])) * Map.blockSize

    def calculatePoints(self):
        top_start_left = Position(self.offsetLeft + self.topleft[0], self.offsetTop + self.topleft[1])
        top_end_left = top_start_left + Position(0, self.top_road_length)
        top_start_right = top_start_left + Position(self.top_road_width, 0)
        top_end_right = top_start_right + Position(0, self.top_road_length)
        self.topPoints = ((top_start_left, top_end_left), (top_start_right, top_end_right))

        left_start_up = top_end_left.copy()
        left_end_up = left_start_up + Position(-self.left_road_length, 0)
        left_start_down = left_start_up + Position(0, self.left_road_width)
        left_end_down = left_end_up + Position(0, self.left_road_width)
        self.leftPoints = ((left_start_up, left_end_up), (left_start_down, left_end_down))

        right_start_up = top_end_right.copy()
        right_end_up = right_start_up + Position(self.right_road_length, 0)
        right_start_down = right_start_up + Position(0, self.right_road_width)
        right_end_down = right_end_up + Position(0, self.right_road_width)
        self.rightPoints = ((right_start_up, right_end_up), (right_start_down, right_end_down))

        down_start_left = left_start_down.copy()
        down_end_left = down_start_left + Position(0, self.down_road_length)
        down_start_right = right_start_down.copy()
        down_end_right = down_start_right + Position(0, self.down_road_length)
        self.downPoints = ((down_start_left, down_end_left), (down_start_right, down_end_right))

    def seal(self, screen):
        if self.left_road_length <= 0:
            draw_line(screen, self.leftPoints[0][0], self.leftPoints[1][0])
        if self.right_road_length <= 0:
            draw_line(screen, self.rightPoints[0][0], self.rightPoints[1][0])
        if self.top_road_length <= 0:
            draw_line(screen, self.topPoints[0][0], self.topPoints[1][0])
        if self.down_road_length <= 0:
            draw_line(screen, self.downPoints[0][0], self.downPoints[1][0])

    def prepare(self, screen):
        pygame.display.set_caption("Game")
        screen.fill(WHITE)

    def draw(self, screen):
        self.drawDirections(screen, [self.topPoints, self.rightPoints, self.leftPoints, self.downPoints])
        self.seal(screen)

    def drawDirections(self, screen, directions):
        for dir in directions:
            draw_line(screen, dir[0][0], dir[0][1])
            draw_line(screen, dir[1][0], dir[1][1])
