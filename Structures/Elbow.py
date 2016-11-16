import pygame
import logging
from Structures.Road import Road
from Structures.Turn import Turn
from Structures.Structure import Structure
from Structures.CrossRoad import CrossRoad
from Structures.Structure import Directions

logging.basicConfig(level=logging.INFO, filename='Logs/elbow.log', filemode='w')
logger = logging.getLogger(__name__)


class Elbow(Structure):
    def __init__(self, position: list, size: int, dir1: int, dir2: int):
        ratio = 0.55
        super(Elbow, self).__init__(position, ratio * size, ratio * size)
        self.structures = []
        """list[Structures.Structure.Structure]"""
        self.initStructures(size, dir1, dir2)

        """:type : list[Structures.Structure.Structure]"""

    def initStructures(self, size, dir1, dir2):
        turnHeight = Road.height
        roadLen = int(size - turnHeight / 2)
        road1 = Road(roadLen, None, None, self.position, dir1)
        road2 = Road(roadLen, None, None,
                     [self.position[0] + roadLen, self.position[1] + turnHeight], dir2)
        turn = Turn([self.position[0] + roadLen, self.position[1]], turnHeight, road2, road1)
        road1.connected[0] = turn
        road2.connected[1] = turn
        self.structures.append(road1)
        self.structures.append(road2)
        self.structures.append(turn)

    def render(self, screen):
        for struct in self.structures:
            struct.render(screen)

    def register(self, movable, dir: int):
        assert 0 <= dir <= 1
        if dir == 0:
            self.structures[0].register(movable, dir)
        if dir == 2:
            self.structures[1].register(movable, dir)

    def update(self):
        for str in self.structures:
            str.update()
