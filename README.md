Similarity-join
=========

This package contains modules for doing (in-memory) similarity joins (aka [approximate string matching](http://en.wikipedia.org/wiki/Approximate_string_matching)).

The package currently contains two modules.

triejoin
------------
This module allows for joins between two sets of strings subject to a similarity constrain (edit distance). The algorithms implemented are inspired by [1].

Please refer to [my site](http://procrastinaty.com/projects/) for the documentation.

cosinejoin
------------
This module does approximate string matching using cosine similarity as a distance metric.

Bibliography
------------
[1] - Trie-Join:Efficient Trie-based String Similarity Joins with Edit Distance Constraints; Jiannan Wang, Jianhua Feng, Guoliang Li.
