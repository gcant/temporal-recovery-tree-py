import networkx as nx
import numpy as np

class Node:
    def __init__(self, n_min, n_max, W):
        self.parent = -1
        self.l = -1
        self.r = -1
        self.n_min = n_min
        self.n_max = n_max
        self.W = W
        self.data = []

class BoundarySampler:
    def __init__(self, n):
        self.node = []
        unrooted_nodes = []
        K = int( np.ceil( np.log2( n ) ) )
        for i in range(K):
            self.node.append( Node(2**i, 2**(i+1), 0) )
            unrooted_nodes.append(i)
        while len(unrooted_nodes) > 1:
            new_unrooted = []
            for i in range(0,len(unrooted_nodes)-1,2):
                k = len(self.node)
                i,j = unrooted_nodes[i], unrooted_nodes[i+1]
                n_min = min( self.node[i].n_min, self.node[j].n_min )
                n_max = max( self.node[i].n_max, self.node[j].n_max )
                W = self.node[i].W + self.node[j].W
                self.node.append( Node(n_min, n_max, W) )
                self.node[-1].l = i
                self.node[-1].r = j
                self.node[i].parent = k
                self.node[j].parent = k
                new_unrooted.append(k)
            if len(unrooted_nodes)%2 == 1:
                new_unrooted.append(unrooted_nodes[-1])
            unrooted_nodes = new_unrooted



    def sum(self):
        return self.node[-1].W

    
    def random_leaf(self):
        ans = len(self.node)-1
        while self.node[ans].l > -1:
            if np.random.randint(self.node[ans].W) < self.node[self.node[ans].l].W:
                ans = self.node[ans].l
            else:
                ans = self.node[ans].r
        return ans

    def random_draw(self):
        node = self.random_leaf()
        while True:
            i = np.random.randint(len( self.node[node].data ))
            if np.random.random() < float(self.node[node].data[i][1]) / self.node[node].n_max:
                break
        ans = self.node[node].data[i]
        self.node[node].data[i] = self.node[node].data[-1]
        self.node[node].data.pop()
        self.node[node].W = self.node[node].W - ans[1]
        while self.node[node].parent > -1:
            node = self.node[node].parent
            self.node[node].W = self.node[ self.node[node].l ].W + self.node[ self.node[node].r ].W
        return ans

    def find_node(self, data):
        ans = len(self.node)-1
        while self.node[ans].l > -1:
            l,r = self.node[ans].l, self.node[ans].r
            if self.node[r].n_min <= data[1] <= self.node[r].n_max:
                ans = r
            else:
                ans = l
        return ans

    def add(self, data):
        node = self.find_node(data)
        self.node[node].data.append(data)
        self.node[node].W = self.node[node].W + data[1]
        while self.node[node].parent > -1:
            node = self.node[node].parent
            self.node[node].W = self.node[ self.node[node].l ].W + self.node[ self.node[node].r ].W

    def draw(self):
        return self.random_draw()

