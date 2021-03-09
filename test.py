import numpy as np
import networkx as nx
from temporal_recovery import *
import full_marginal

# Generate a tree network
G = nx.barabasi_albert_graph(40,1)

# Compute the seed probabilties, where p[v] is the probability that node v is the first to have appeared.
p = compute_p(G)

# Create an empty list of histories
H = []

# Sample 500 histories
for i in range(500):
    # For each history select seed proportionally to the seed probability
    seed = np.random.choice( np.arange(G.number_of_nodes()), p=p)
    # Interpolate between that seed and the fulll history
    H.append([seed]+interpolate(G, seed, G.neighbors(seed)))
  
# Compute the (Monte Carlo) probability distribution over arrival times for all nodes
H = np.array(H)
P_MC = np.array([np.mean(H==i,axis=0) for i in range(G.number_of_nodes())])

# Compute the (exact) probability distribution over arrival times for all nodes
P_exact = full_marginal.one_node_marginals(G)

# Compute the mean arrival times from the Monte Carlo and exact probability distributions.
mean_MC = np.dot(P_MC, np.arange(G.number_of_nodes()))
mean_exact = np.dot(P_exact, np.arange(G.number_of_nodes()))

# Compare results
print(mean_exact)
print(mean_MC)

