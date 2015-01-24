import itertools as it                                                           
                                                                                 
class PeekableIterator:                                                          
    def __init__(self, iterator):                                                
        self.it = iterator                                                       
        self._next = None                                                        
                                                                                 
    def __iter__(self):                                                          
        return self                                                              
                                                                                 
    def next(self):                                                              
        current = self.peek()                                                    
        self._next = None                                                        
        return current                                                           
                                                                                 
    def peek(self):                                                              
        self._next = self._next if self._next else self.it.next()                
        return self._next                                                        
                                                                                 
    def has_next(self):                                                          
        try:                                                                     
            self.peek()                                                          
        except:                                                                  
            return False                                                         
        return True                                                              
                                                                                 
                                                                                 
def q_grams(string, q=3, pad='_', trim=True):                                     
    string = string.strip() if trim else string                                     
    string = pad + string + pad if pad else string                                  
                                                                                 
    iters = [it.islice(string, i, None) for i in range(q)]                        
    return [''.join(q_gram) for q_gram in zip(*iters)]                           
                                                        
def to_dot(trie, out="out.dot"):
    f = open(out, 'w')

    f.write("digraph G {\n")
    for n in trie.pre_order():
        f.write("  %s [color=%s,label=\"%s\"];\n" 
            % ('R'+n.prefix(), "red" if n in trie._terminals else "black", n._element))

    for n in trie.pre_order():
        for c in n:
            f.write("  %s -> %s;\n" % ('R'+n.prefix(), 'R'+c.prefix()))
    f.write("}")
    f.close()

