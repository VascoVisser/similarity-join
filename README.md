Similarity-join
=========

This package contains modules for doing (in-memory) similarity joins (i.e., [approximate string matching](http://en.wikipedia.org/wiki/Approximate_string_matching) between lists).

A similarity join finds similar records in lists. Given two lists of strings (called records) R and S, a similarity join will find for each record in R all records in S that are similar. Similarity is defined by a distance metric. The choice of metric is use-case specific.

The package currently contains two modules.

cosinejoin
------------
This module does approximate string matching using cosine similarity as a distance metric. The module comes with an option to approximate the results. Approximation greatly reduces time and memory foodprints.

The module creates an intermediate representation of the dataset that becomes quite large. Your data too big for this module? A cosine join can be implemented in SQL [2].

triejoin
------------
This module allows for joins between two sets of strings subject to a similarity constrain (edit distance). The algorithms implemented are inspired by [1].

Please refer to [my site](http://procrastinaty.com/projects/) for the documentation.

Bibliography
------------
[1] - Trie-Join:Efficient Trie-based String Similarity Joins with Edit Distance Constraints; Jiannan Wang, Jianhua Feng, Guoliang Li.

[2] - Text joins in an RDBMS for web data integration. Gravano, L., Ipeirotis, P. G., Koudas, N., & Srivastava, D.
