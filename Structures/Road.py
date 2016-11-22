from DataStructures.List import List, Node, SingleNode
import pygame


class Road:
    def __init__(self, ):
        self.startNode = RoadNode([0, 0], [0, 0], lambda x: [x[0] + 10, x[1]], lambda: [0, 10])
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
    def __init__(self, microNodes: list, pointA, calculateB, calculateVector):
        super().__init__(microNodes)
        self.microNodes = microNodes
        self.pointA = pointA
        self.calculateB = calculateB
        self.calculateVector = calculateVector
        self.pointB = calculateB(pointA)
        self.vector = calculateVector()

    def CreateNext(self, micronodes):
        node = RoadNode(micronodes, self.pointB, self.calculateB, self.calculateVector)
        self.connect(node)
        return node

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, (0, 0, 0), self.pointA, self.getSecondPoint(self.pointA), 2)

    def getSecondPoint(self, pointA):
        return [pointA[0] + 10, pointA[1]]
