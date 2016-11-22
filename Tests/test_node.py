import unittest
from unittest import TestCase

from DataStructures.List import SingleNode


class TestNode(TestCase):
    def setUp(self):
        self.nodes = [SingleNode(i) for i in range(300)]

        for i in range(1, 300):
            self.nodes[i - 1].connect(self.nodes[i])

    def tests_connection_by_value(self):
        q = 0
        node = self.nodes[0]
        while node is not None:
            self.assertIsInstance(node, SingleNode)
            self.assertEqual(q, node.data)
            q += 1
            node = node.next[0] if node.next is not None and len(node.next) > 0 else None

    def test_connection_by_reference(self):
        node = self.nodes[0]
        current = self.nodes[1]
        print(self.nodes[0].next[0])
        print(self.nodes[1])
        self.assertIsNone(node.prev)
        self.assertIs(node.next[0], current)
        prev = self.nodes[0]
        while current is not None:
            self.assertIs(current.prev, prev, "is : {0}, should be :{1}".format(current.prev.data, current.data))
            current = current.next[0]
            prev = prev.next[0]


if __name__ == '__main__':
    unittest.main()
