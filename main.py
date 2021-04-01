import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from Node import Node, Port
from pprint import pprint
from collections import defaultdict


def get_bin(x, n=0):
    return format(x, 'b').zfill(n)


G = nx.Graph()

G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
G.add_edges_from([(1, 2), (1, 3), (1, 4),
                  (2, 3), (2, 4),
                  (3, 4),
                  (4, 5), (4, 6), (4, 7), (4, 8),
                  (5, 6), (5, 7), (5, 8),
                  (6, 7), (6, 8), (6, 9), (6, 10),
                  (7, 11), (7, 12),
                  (9, 10),
                  (11, 12),
                  (12, 13), (12, 14), (12, 15),
                  (14, 16), (14, 17),
                  (15, 18), (15, 21),
                  (16, 17),
                  (18, 19), (18, 20),
                  (21, 22), (21, 23), (21, 24),
                  (22, 23), (22, 24),
                  (23, 24)])

nx.draw(minimum_spanning_tree(G), with_labels=True, font_weight='bold')
plt.show()

print('Number of Nodes:', G.number_of_nodes())

nodes = [Node(1, [Port(1, 2), Port(1, 3), Port(1, 4)]),
         Node(2, [Port(1, 2), Port(2, 3), Port(2, 4)]),
         Node(3, [Port(1, 3), Port(2, 3), Port(3, 4)]),
         Node(4, [Port(1, 4), Port(2, 4), Port(3, 4), Port(4, 5), Port(4, 6), Port(4, 7), Port(4, 8)]),
         Node(5, [Port(4, 5), Port(5, 6), Port(5, 7), Port(5, 8)]),
         Node(6, [Port(4, 6), Port(5, 6), Port(6, 7), Port(6, 8), Port(6, 9), Port(6, 10)]),
         Node(7, [Port(4, 7), Port(5, 7), Port(6, 7), Port(7, 8), Port(7, 11), Port(7, 12)]),
         Node(8, [Port(4, 8), Port(5, 8), Port(6, 8), Port(7, 8)]),
         Node(9, [Port(6, 9), Port(9, 10)]),
         Node(10, [Port(6, 10), Port(9, 10)]),
         Node(11, [Port(7, 11), Port(11, 12)]),
         Node(12, [Port(6, 12), Port(11, 12), Port(12, 13), Port(12, 14), Port(12, 15)]),
         Node(13, [Port(12, 13)]),
         Node(14, [Port(12, 14), Port(14, 16), Port(14, 17)]),
         Node(15, [Port(12, 15), Port(15, 18), Port(15, 21)]),
         Node(16, [Port(14, 16), Port(16, 17)]),
         Node(17, [Port(14, 17), Port(16, 17)]),
         Node(18, [Port(15, 18), Port(18, 19), Port(18, 20)]),
         Node(19, [Port(18, 19)]),
         Node(20, [Port(18, 20)]),
         Node(21, [Port(15, 21), Port(21, 22), Port(21, 23), Port(21, 24)]),
         Node(22, [Port(21, 22), Port(22, 23), Port(22, 24)]),
         Node(23, [Port(21, 23), Port(22, 23), Port(23, 24)]),
         Node(24, [Port(21, 23), Port(22, 24), Port(23, 24)])]

robot_pos = 1
# Map oracle = 0 , Instance oracle = 1
oracle = 0
if oracle == 0:
    edges = nx.dfs_labeled_edges(minimum_spanning_tree(G), robot_pos)
else:
    edges = nx.dfs_labeled_edges(minimum_spanning_tree(G), random.randint(1, G.number_of_nodes()))

path = []
node_path = []
back_source = []
ports = []
visited_nodes = 0
bit = math.ceil(math.log(G.number_of_nodes(), 2))
print('bit:', bit)
for u, v, d in edges:
    found = False
    if visited_nodes != G.number_of_nodes():
        if d == "forward":
            path.append(1)
            node_path.append(v)
            visited_nodes += 1
            for nod in nodes:
                k = 0
                for por in nod.ports:
                    if u == por.n1 and v == por.n2:
                        ports.append(get_bin(k, bit))
                        found = True
                    k += 1
                if found:
                    break
        elif d == 'reverse':
            path.append(0)
            node_path.append(u)
            for nod in reversed(nodes):
                k = 0
                for por in nod.ports:
                    if u == por.n1 and v == por.n2:
                        ports.append(get_bin(k, bit))
                        found = True
                    k += 1
                if found:
                    break
    elif d == 'reverse':
        back_source.append(0)

print('Structure of the graph (1:forward, 0:reverse): ', path)
print('Back to the source: ', back_source)
print('DFS sequence of nodes: ', node_path)
print('DFS sequence of ports: ', ports)
