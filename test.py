import numpy as np
import networkx as nx
from temporal_recovery import *
import full_marginal

G = nx.barabasi_albert_graph(40,1)

p = compute_p(G)
H = []
for i in range(500):
    seed = np.random.choice( np.arange(G.number_of_nodes()), p=p )
    H.append([seed]+interpolate(G, seed, G.neighbors(seed)))
H = np.array(H)
P_MC = np.array([np.mean(H==i,axis=0) for i in range(G.number_of_nodes())])

P_exact = full_marginal.one_node_marginals(G)
P_exact /= np.sum(P_exact[0])

mean_MC = np.dot(P_MC, np.arange(G.number_of_nodes()))
mean_exact = np.dot(P_exact, np.arange(G.number_of_nodes()))

print(mean_exact)
print(mean_MC)

