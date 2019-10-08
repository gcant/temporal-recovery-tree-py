# temporal-recovery-tree-py
Python implementation of efficient tree history algorithms.

Sampling requires networkx and numpy.
Full one-node marginals additionally requires mpmath.

- temporal_recovery.py contains our algorithms for recovering the history of a tree.

- boundary_sampler.py is a Python implementation of the data structure described in section 3.2.2 of:<br>
G. St-Onge, J.-G. Young, L. Hébert-Dufresne, and L. J. Dubé, Efficient sampling of spreading processes on complex networks using a composition and rejection algorithm.<br>
We use this to sample efficiently from the boundary set.<br>

- full_marginal.py contains our algorithms for the one-node marginals.
