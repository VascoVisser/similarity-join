
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

