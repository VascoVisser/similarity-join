import itertools as it
from collections import deque

from Levenshtein import distance
from transactionaldict import TransactionalDict as tdict

class Trie:

    _root = None
    _terminals = None
    _collection_count = None

    def __init__(self):
        self._root = Node(element='')
        self._terminals = set()
        self._collection_count = 1

    def add(self, seq, collection_mask):
        node = self._root
        for e in seq:
            node = node.add_or_fetch_child(e)
            node._member_of = node._member_of | collection_mask
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

    @staticmethod
    def calc_active_node_set(node, parent_node_set, sigma):
        active_nodes = []
        for n, ed in parent_node_set.items():
            if ed < sigma:
                active_nodes.append((n, ed+1))

            for nc in n._child_nodes:
                if not nc._visited:
                    continue
                if nc._element == node._element:
                    active_nodes.append((nc, ed))
                    if ed < sigma and nc != node:
                        for ncc,d in nc.breadth_first(sigma-ed):
                            active_nodes.append((ncc, ed+d))
                elif ed < sigma:
                    active_nodes.append((nc, ed+1))

        return dict(sorted(active_nodes, key=lambda x: x[1], reverse=True))
    
    def trie_search(self, seq, sigma):
        node = self._root
        stack = [None]
        while node:
            if node in self._terminals and node.is_active(seq, sigma):
                yield node
            if not node.can_prune(seq, sigma):
                for child in node:
                    stack.append(child)
            node = stack.pop()

    def _index(self, collection, collection_id):
        for w in collection:
            self.add(w, collection_id)

    def index(self, collection1, collection2=None):
        self._index(collection1, 1)
        if collection2:
            self._collection_count = 2
            self._index(collection2, 2)
   
    def _self_join(self, sigma):
    
        for n in self._root.pre_order():
            n._visited = False
        
        active_node_stack = [{self._root : 0}]
        self._root._visited = True

        traversal_stack = [None] + [c for c in self._root]
        node = traversal_stack.pop()

        while node:
            node._visited = True

            # Calculate this node's active node set
            parent_active_nodes = active_node_stack[-1]
            active_node_set = self.calc_active_node_set(
                node, parent_active_nodes, sigma)

            # Update active node sets of ancestors
            for ancestor_active_node, cnt in zip(
                    active_node_stack[-1:-sigma-1:-1], it.count(start=1)):
                if (not node in ancestor_active_node or 
                        cnt < ancestor_active_node[node]):
                    ancestor_active_node[node] = cnt

            # Possibly generate results
            if node in self._terminals:
                for output_candidate in active_node_set:
                    if (output_candidate in self._terminals and 
                            output_candidate != node):
                        yield (node, output_candidate)

            # Push child nodes on traversal stack
            traversal_stack.extend(child for child in node._child_nodes)
            
            next_node = traversal_stack.pop()
            # active_node_stack book keeping
            if next_node and next_node._parent == node:
                # went down
                active_node_stack.append(active_node_set)
            elif next_node and next_node._parent == node._parent:
                # stay on same level
                pass
            elif next_node:
                # went up
                for a in node.move_up():
                    active_node_stack.pop()
                    if a._parent == next_node._parent:
                        break
            node = next_node
    
    def join(self, sigma):
       if self._collection_count < 2:
           return self._self_join(sigma)
        

class Node:
    _child_nodes = None
    _parent = None
    _element = None
    _member_of = None
             
    def __init__(self, element=None, parent=None):
        self._element = element
        self._parent = parent
        self._child_nodes = []
        self._member_of = 0

    def prefix(self):
        stack = []
        node = self
        while node._parent:
            stack.append(node._element)
            node = node._parent
        return ''.join(reversed(stack))
                   
    def add_or_fetch_child(self, element):
        """ Create and/or fetch a child that has element

        If this node has a child with element, then return
        that child. Otherwise create a node with element,
        add the node to this node and then return it.
        """

        child = self.child_by_element(element)
        if not child:
            child = Node(element, self)
            self._child_nodes.append(child)
        return child
    
    def child_by_element(self, element):
        """ Return a child iff it has element """
        for c in self._child_nodes:
            if c._element == element:
                return c
  
    def is_active(self, test_seq, sigma):
        node_prefix = self.prefix()
        return distance(node_prefix, test_seq) <= sigma

    def can_prune(self, test_seq, sigma):
        node_prefix = self.prefix()
        for i in range(len(test_seq) + 1):
            prefix = test_seq[:i]
            if self.is_active(prefix, sigma):
                return False
        return True
   
    def is_ancestor(self, node):
        for a in node.move_up():
            if self == node._parent:
                return True
        return False
    
    def move_up(self):
        node = self
        while node._parent:
            yield node._parent
            node = node._parent

    def pre_order(self):
        """ Pre_order traversal starting at the root """ 
        node = self 
        stack = [None]
        while node:
            yield node
            stack.extend(reversed(node._child_nodes))
            node = stack.pop()

    def breadth_first(self, max_rel_depth=None):
        dq = deque((n, 1) for n in self)
        while dq:
            n,d = dq.popleft()
            yield n,d
            d_ = d + 1
            if not max_rel_depth or d_ <= max_rel_depth:
                for n_ in n:
                    dq.append((n_,d_))

    def __str__(self):
        return 'Node(%s)' % (self.prefix() if 
            self._parent else '-ROOT-',)
    
    def __repr__(self):
        return '<Node(%s)>' % (self.prefix() if 
            self._parent else '-ROOT-',)
     
    def __iter__(self):
        return (c for c in self._child_nodes)
