import pygame

from drawing.drawing_consts import BLACK, BLUE
from drawing.drawing_consts import CAR_RADIUS


def draw_line(screen, point1, point2, color=BLACK):
    """
    Draws a line between two points on the screen using selected color
    :return: None
    """
    pygame.draw.line(screen, color, [point1.x, point1.y], [point2.x, point2.y])


def draw_circle(screen, position, radius, color=BLACK):
    """
    Draws a circle in selected color and position
    :return: None
    """
    pygame.draw.circle(screen, color, [position.x, position.y], radius)


def draw_car_by_value(screen, position, value):
    color = (255, 255, 255)
    if value == 0:
        color = (200, 0, 0)
    if value == 1:
        color = (0, 200, 0)
    if value == 2:
        color = (0, 0, 200)  # magenta
    if value == 3:
        color = (255, 0, 114)
    if value == 4:
        color = (0, 0, 0)
    draw_car(screen, position, color)


def draw_car(screen, position, color=BLUE):
    """
    Draws a car in selected color and position
    :return: None
    """
    draw_circle(screen, position, CAR_RADIUS, color)
