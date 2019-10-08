import networkx as nx
import numpy as np
import boundary_sampler

### Functions for seed finding algorithm 
def recursive_n(G, n, i):
    n[i] = 1+np.sum([recursive_n(G, n, j) for j in G.successors(i)])
    return n[i] 

def recursive_p(G, n, p, i):
    for j in G.successors(i):
        p[j] = p[i] * n[j] / (G.number_of_nodes() - n[j])
        recursive_p(G, n, p, j)

def compute_p(G):
    G0 = nx.bfs_tree(G,0)
    n0,p = np.zeros(G.number_of_nodes()), np.ones(G.number_of_nodes())
    recursive_n(G0, n0, 0)
    recursive_p(G0, n0, p, 0)
    return p / np.sum(p)


### Function for sampling interpolations
def interpolate(G, seed, initial_boundary):
    G_seed = nx.bfs_tree(G, seed)
    n = np.zeros(G_seed.number_of_nodes())
    recursive_n(G_seed, n, seed)
    B = boundary_sampler.BoundarySampler( G_seed.number_of_nodes() )
    history = []
    for i in initial_boundary:
        B.add( (i, n[i]) )
    while B.sum()>0:
        j = B.draw()[0]
        for k in G_seed.successors(j):
            B.add( (k, n[k]) )
        history.append(j)
    return history


### Function to return current boundary, given partial history
### (this isn't needed to simulate full histories)
def boundary(G, extant_nodes):
    b = set()
    for node in extant_nodes:
        b = b.union(G.neighbors(node))
    for node in extant_nodes:
        b.remove(node)
    return list(b)

### example
if __name__=="__main__":
    G = nx.barabasi_albert_graph(100,1)
    p = compute_p(G)
    seed = np.random.choice( np.arange(G.number_of_nodes()), p=p )
    history = interpolate(G, seed, G.neighbors(seed))
    print(history)
