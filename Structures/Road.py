from DataStructures.List import List, Node, SingleNode
import pygame


class TurnNode(Node):
    def __init__(self, microNodes: list, pointA, calculateB, vector, strip=False):
        super().__init__(microNodes)
        self.next = [None, None, None, None]  # type: List[RoadNode]
        self.pointA = pointA
        self.vector = vector
        self.calculateB = calculateB
        self.microNodes = microNodes
        self.setLeft()

    def CreateNext(self, pointA, calculateB, calculateVector):
        node = RoadNode([0, 0], pointA, calculateB, calculateVector, True)
        return node

    def setRight(self):
        calculateVector = [-self.vector[1], self.vector[0]]
        calculateB = [-self.calculateB[1], self.calculateB[0]]
        self.next[0] = self.CreateNext(self.pointA, calculateB, calculateVector)

    def setForward(self, node):
        self.next[3] = node

    def setLeft(self):
        calculateVector = [self.vector[1], -self.vector[0]]
        calculateB = [self.calculateB[1], -self.calculateB[0]]
        self.next[0] = self.CreateNext(self.pointA, calculateB, calculateVector)

    def render(self, surface):
        pass

class RoadNode(SingleNode):
    def __init__(self, microNodes: list, pointA, calculateB, vector, strip=False):
        super().__init__(microNodes)
        self.microNodes = microNodes
        self.pointA = pointA
        self.calculateB = calculateB
        self.vector = vector
        self.strip = strip
        self.calculate()

    def calculate(self):
        self.pointB = [self.pointA[0] + self.calculateB[0], self.pointA[1] + self.calculateB[1]]

    def CreateNext(self, micronodes):
        node = RoadNode(micronodes, self.pointB, self.calculateB, self.vector, not self.strip)
        self.connect(node)
        return node

    def __str__(self):
        return "Position = [{0},{1}], data = {2}".format(self.pointA, self.pointB, self.microNodes)

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, (0, 255, 0), self.pointA, self.pointB, 2)
        pygame.draw.line(surface, (0, 0, 255), RoadNode.movePoint(self.pointA, self.vector),
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
            carPos = [int((self.pointB[0] - self.pointA[0]) / 2 + vect[0] + self.pointA[0]),
                      int((self.pointB[1] - self.pointA[1]) / 2 + vect[1] + self.pointA[1])]
            pygame.draw.circle(surface, (255, 0, 0), carPos, 5)


class Road:
    def __init__(self, start):
        self.startNode = RoadNode([-1, 0], start, [3, 0], [0, 30], True)  # type: RoadNode
        current = self.startNode
        data = [-1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(110):
            if (i > 5):
                n = current.CreateNext([0, 0])
            else:
                n = current.CreateNext([data[i], 0])
            current = n
        self.startNode = self.startNode.next[0].next[0]
        self.list = List(self.startNode)
        current.microNodes[0] = 1

    def render(self, surface):
        for node in self.list.bfs():
            node.render(surface)

    def addCar(self):
        self.startNode.microNodes[0] = 2

    def printList(self):
        for node in self.list.bfs():
            print(node.data, end=' ')
        print("")

    def refresh(self):
        # concurency method?
        # TODO: refresh for prev
        self.refreshNext()

    def find_first_empty(self, node: RoadNode):
        if node is None or node.next is None or node.next[0] is None:
            print("Raise error0")
            raise IndexError
        while node is not None and node.microNodes[0] != 0:
            if node.next is None:
                print("Raise error1")
                raise IndexError
            node = node.next[0]
        if node is None or node.microNodes[0] != 0:
            print("Raise error2")
            raise IndexError
        return node

    def refreshNext(self):
        current = self.startNode  # type: RoadNode
        """:type : Structures.RoadNode"""
        while True:
            try:
                last = currentPrev = self.find_first_empty(current)  # type: RoadNode
                while currentPrev is not current and currentPrev.prev is not None:
                    currentPrev.microNodes[0] = currentPrev.prev.microNodes[0]
                    currentPrev = currentPrev.prev
                # currentPrev.prev is none or currentprev==current
                current.microNodes[0] = 0
                current = last.next[0]
            except IndexError:
                break
        if current is not None:
            current.microNodes[0] = 0 if current.microNodes[0] <= 1 else current.microNodes[0] - 1
        self.startNode.microNodes[0] = 0
