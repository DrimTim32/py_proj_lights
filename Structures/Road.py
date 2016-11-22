from DataStructures.List import List, Node, SingleNode
import pygame


class Road:
    def __init__(self, ):
        self.startNode = RoadNode([2, 0], [0, 0], lambda x: [x[0] + 10, x[1]], lambda: [0, 30], True)
        current = self.startNode
        for i in range(30):
            n = current.CreateNext([current.data[0] + 1, current.data[1] + 1])
            current = n
        self.list = List(self.startNode)

    def render(self, surface, start):
        for node in self.list.bfs():
            print(node.data)
            node.render(surface)


class RoadNode(SingleNode):
    def __init__(self, microNodes: list, pointA, calculateB, calculateVector, strip=False):
        super().__init__(microNodes)
        self.microNodes = microNodes
        self.pointA = pointA
        self.calculateB = calculateB
        self.calculateVector = calculateVector
        self.pointB = calculateB(pointA)
        self.vector = calculateVector()
        self.strip = strip

    def CreateNext(self, micronodes):
        node = RoadNode(micronodes, self.pointB, self.calculateB, self.calculateVector, not self.strip)
        self.connect(node)
        return node

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, (0, 0, 0), self.pointA, self.pointB, 2)
        pygame.draw.line(surface, (0, 0, 0), RoadNode.movePoint(self.pointA, self.vector),
                         RoadNode.movePoint(self.pointB, self.vector), 2)
        if self.strip:
            vect = [self.vector[0] / 2, self.vector[1] / 2]
            pygame.draw.line(surface, (0, 0, 0), RoadNode.movePoint(self.pointA, vect),
                             RoadNode.movePoint(self.pointB, vect), 2)
        self.drawCar(surface)

    @staticmethod
    def movePoint(point, vector):
        return [point[0] + vector[0], point[1] + vector[1]]

    def drawCar(self, surface):
        if self.microNodes[0] == 2:
            vect = [(3 * self.vector[0]) / 4, (3 * self.vector[1]) / 4]
            carPos = [int((self.pointB[0] - self.pointA[0]) / 2 + vect[0]),
                      int((self.pointB[1] - self.pointA[1]) / 2 + vect[1])]
            pygame.draw.circle(surface, (255, 0, 0), carPos, 5)
