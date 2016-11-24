class Node:
    def __init__(self, data):
        self.data = data
        self._next = [None]
        self.prev = None

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, value):
        self._next = value

    def connect(self, Node2):
        """ Connects current node to Node2 (self is prev to Node2) """
        if self.next is not None and Node2 not in self.next:
            self.next.append(Node2)
        Node2.prev = self


class SingleNode(Node):
    def __init(self, data):
        super(type(SingleNode)).__init__(data)

    def connect(self, Node2):
        self._next[0] = Node2
        Node2.prev = self


class List:
    def __init__(self, head):
        self.head = head

    def bfs(self, current=None):
        current = self.head if current is None else current
        return List.doBfs(current)

    @staticmethod
    def doBfs(current):
        if current is None or current.next is None:
            raise StopIteration
        yield current
        for node in current.next:
            yield from List.doBfs(node)
