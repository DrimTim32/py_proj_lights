"""
All consts important for drawing map and cars.
In the name of 'Namespaces are one honking great idea -- let's do more of those!' rule
"""

#region Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
MINIMUM_OFFSET = 100
#endregion

BLOCK_SIZE = 20
CONST_OFFSET = 30
CAR_OFFSET = 3
CAR_RADIUS = int((BLOCK_SIZE - 2 * CAR_OFFSET) / 2)

LENGTH_MULTIPLIER = BLOCK_SIZE
WIDTH_MULTIPLIER = BLOCK_SIZE
