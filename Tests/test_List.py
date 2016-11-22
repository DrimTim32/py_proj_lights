import unittest
from unittest import TestCase

from DataStructures.List import Node, List


class TestList(TestCase):
    def test_one(self):
        node1 = Node(1)
        node2 = Node(2)
        nodes0 = [Node(2.1), Node(2.5), Node(2.8)]
        nodes1 = [Node(2.11), Node(2.12), Node(2.13)]
        nodes2 = [Node(2.51), Node(2.52)]
        node1.connect(node2)
        for node in nodes0:
            node2.connect(node)
        for node in nodes1:
            nodes0[0].connect(node)
        for node in nodes2:
            nodes0[1].connect(node)
        list = List(node1)
        output = [1, 2, 2.1, 2.5, 2.8, 2.11, 2.12, 2.13, 2.51, 2.52]
        q = 0
        for node in list.bfs():
            self.assertEqual(node.data, output[q])


if __name__ == '__main__':
    unittest.main()
