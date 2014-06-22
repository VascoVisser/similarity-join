from node import Node
from itertools import izip_longest
from Levenshtein import distance

class Trie:

    _root = None
    _terminals = None

    def __init__(self):
        self._root = Node()
        self._terminals = set()

    def add(self, seq):
        node = self._root
        for e in seq:
            node = node.add_or_fetch_child(e)
        self._terminals.add(node)
          
    def items(self):
        for i in self._terminals:
            yield i.prefix()
     
    def longest_prefix(self, seq):
        node = self._root
        iter = (i for i in seq)

        for i in seq:
            child = node.child_by_element(i)
            if not child:
                break
            node = child
        
        return node

    def pre_order(self):
        """ Pre_order traversal starting at the root """ 
        node = self._root
        stack = [None]
        while node:
            yield node
            for child in node:
                stack.append(child)
            node = stack.pop()

    @staticmethod
    def levensthein(sigma):
        def curried(seq1, seq2):
            return distance(seq1, seq2) <= sigma
        return curried
    
    def trie_search(self, seq, sigma, func=None):
        node = self._root
        stack = [None]
        func = func if func else self.levensthein
        while node:
            if node in self._terminals and node.is_active(seq, func(sigma)):
                yield node
            if not node.can_prune(seq, func(sigma)):
                for child in node:
                    stack.append(child)
            node = stack.pop()
            

    
       







        
