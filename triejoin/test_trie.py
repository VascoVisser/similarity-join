import unittest

from trie import Node

class TrieTestCase(unittest.TestCase):
    pass


class NodeTestCase(unittest.TestCase):
    
    def test_pre_order_one(self):
        root = node = Node()
        for l in 'ABCDE':
            node = node.add_or_fetch_child(l)
        po = [n._element for n in root.pre_order() if n._element != None]
        map(self.assertEqual, po, 'ABCDE')

    def test_pre_order_two(self):
        root = Node()
        for l in 'ABCDE':
            root.add_or_fetch_child(l)
        po = [n._element for n in root.pre_order() if n._element != None]
        map(self.assertEqual, po, 'ABCDE')

    def test_pre_order_three(self):
        pass
