"""
All consts important for drawing map and cars.
In the name of 'Namespaces are one honking great idea -- let's do more of those!' rule
"""
from math import sqrt

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLOCK_SIZE = 15
MINIMUM_OFFSET = 100
CONST_OFFSET = 30
CAR_RADIUS = int(BLOCK_SIZE / 2)
CAR_OFFSET = int(BLOCK_SIZE * sqrt(2) / 4)
