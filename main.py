import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from Node import Graph, Node, Port, MAP_ORACLE, INSTANCE_ORACLE
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
#plt.show()

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

NewGraph = Graph(G, nodes)

robot_pos = 1

print(NewGraph.encode(MAP_ORACLE, robot_pos))
