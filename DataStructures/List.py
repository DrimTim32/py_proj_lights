class Node:
    def __init__(self, data):
        self.data = data
        self._next = [None]
        self.prev = None

    @property
    def next(self):
        return None if self._next is None or self._next[0] is None else self._next

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
        print("Current = {0}".format(current.data))
        yield current
        if current.next is None:
            return []
        for node in current.next:
            yield node
            yield from List.doBfs(node)
