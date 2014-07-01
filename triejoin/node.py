class Node:
    _child_nodes = None
    _parent = None
    _element = None
    _member_of = None
    _prefix = None
         
    def __init__(self, element=None, parent=None):
        self._element = element
        self._parent = parent
        self._child_nodes = []
        self._member_of = 0
        self._prefix = None

    def prefix(self):
        if not self._prefix:
            stack = []
            node = self
            while node._parent:
                stack.append(node._element)
                node = node._parent
            self._prefix = ''.join(reversed(stack))
        
        return self._prefix
                   
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

    def __str__(self):
        return 'Node(%s)' % (self.prefix() if self._parent else '-ROOT-',)
    
    def __repr__(self):
        return '<Node(%s)>' % (self.prefix() if self._parent else '-ROOT-',)
     
    def __iter__(self):
        return (c for c in self._child_nodes)
