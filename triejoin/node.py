class Node:
    _child_nodes = None
    _parent = None
    _element = None
         
    def __init__(self, element=None, parent=None):
        self._element = element
        self._parent = parent
        self._child_nodes = []

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
  
    def is_active(self, test_seq, distance_func):
        node_prefix = self.prefix()
        return distance_func(node_prefix, test_seq)

    def can_prune(self, test_seq, distance_func):
        node_prefix = self.prefix()
        for i in range(len(test_seq) + 1):
            prefix = test_seq[:i]
            if self.is_active(prefix, distance_func):
                return False
        return True
    
     
    def __iter__(self):
        def children():
            for c in self._child_nodes:
                yield c
        return children()
