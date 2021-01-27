import numpy as np
import networkx as nx
import mpmath

factorial = mpmath.factorial

def binom(x,y):
    if x<0 or y<0:
        return mpmath.mpf("0.0")
    else:
        return mpmath.binomial(x,y)


###############

def one_node_marginals(G,norm=True):

    ### Compute n_{i -> j}

    n = {i : {} for i in range(G.number_of_nodes())}
    
    def n_recursion(i,j):
        if not(j in n[i]):
            ans = 1
            for k in G.neighbors(j):
                if k!=i:
                    ans += n_recursion(j,k)
            n[i][j] = ans
        return n[i][j]
    
    for i,j in G.edges():
        n_recursion(i,j)
        n_recursion(j,i)

    ### n_{i ->j} computed


    ### Compute h_{i -> j}
    
    h = {i : {} for i in range(G.number_of_nodes())}
    
    def h_recursion(i,j):
        if not(j in h[i]):
            ans = factorial(n[i][j]-1)
            for k in G.neighbors(j):
                if k!=i:
                    ans *= h_recursion(j,k)/factorial(n[j][k])
            h[i][j] = ans
        return h[i][j]
    
    for i,j in G.edges():
        h_recursion(i,j)
        h_recursion(j,i)

    ### h_{i ->j} computed


    ### compute g_{i ->j}(t) 

    g = {i : {} for i in range(G.number_of_nodes())}
    for i in G.nodes():
        for j in G.neighbors(i):
            g[i][j] = np.ones(G.number_of_nodes(), dtype=mpmath.mpf)*-1
            g[i][j][0] = 0
            g[i][j][1] = h[i][j]
    
    def f(i,j,k,t):
        return (h[k][j]*binom(n[i][j]-t-1,n[j][k]-t)) / (binom(n[k][j]-1,n[j][i])*h[j][i])
    
    for t in range(1,G.number_of_nodes()-1):
        for i in G.nodes():
            for j in G.neighbors(i):
                temp = g[i][j][t]
                for k in G.neighbors(j):
                    if k!=i:
                        temp += g[j][k][t]*f(i,j,k,t)
                g[i][j][t+1] = temp

    ### g_{i ->j}(t) computed
    
    ### Compute P_i(t), one node marginals
    
    P = np.zeros(( G.number_of_nodes(), G.number_of_nodes() ), dtype=mpmath.mpf )
    
    for i in G.nodes():
        temp = factorial(G.number_of_nodes()-1) 
        for j in G.neighbors(i):
            temp *= h[i][j] / factorial(n[i][j])
        P[i,0] = temp
    
    for t in range(1,G.number_of_nodes()):
        for i in G.nodes():
            temp = 0.0
            for j in G.neighbors(i):
                temp += g[i][j][t] * h[j][i] * binom(G.number_of_nodes()-t-1,n[i][j]-t)
            P[i][t] = temp

    if norm:
        P = P/np.sum(P[0])
    
    return(P.astype(float))
    
