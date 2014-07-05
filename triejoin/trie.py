from node import Node
from itertools import izip_longest
from Levenshtein import distance

class Trie:

    _root = None
    _terminals = None
    _collection_count = None

    def __init__(self):
        self._root = Node(element='')
        self._root._prefix = ''
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
    def calc_active_node_set(node, parent_node_set, sigma):
        prefix = node.prefix()
        node_list = []
        for candidate in parent_node_set:
            if distance(candidate._prefix, prefix) <= sigma:
                node_list.append(candidate)
            # Test all childeren of candidate and add to active set if needed
#            node_list.extend([c for c in (c for c in candidate._child_nodes if c._visited) if \
#                                distance(c._prefix, prefix) <= sigma])
            node_list.extend([c for c in candidate._child_nodes if c._visited and \
                                distance(c._prefix, prefix) <= sigma])
        return set(node_list)
   
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
    
        for n in self.pre_order():
            n._visited = False
        
        active_node_stack = [set([self._root])]
        self._root._visited = True

        traversal_stack = [None] + [c for c in self._root]
        node = traversal_stack.pop()

        while node:
            node._visited = True

            # Calculate this node's active node set
            parent_active_nodes = active_node_stack[-1]
            active_node_set = self.calc_active_node_set(node, parent_active_nodes, sigma)
            # active_node_set = set(n for n in active_node_set if n._visited)

            # Update active node sets of ancestors
            for ancestor_active_node in active_node_stack[-sigma:]:
                ancestor_active_node.add(node)

            # Possibly generate results
            if node in self._terminals:
                for output_candidate in active_node_set:
                    if output_candidate in self._terminals and output_candidate != node:
                        yield (node, output_candidate)

            # Push child nodes on traversal stack
            traversal_stack.extend(child for child in node)
            
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






        
