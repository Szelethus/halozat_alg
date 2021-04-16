import unittest
import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from PortNumberedGraph import PortNumberedGraph
from Oracle import Oracle, MAP_ORACLE, INSTANCE_ORACLE

Graph = PortNumberedGraph()
Graph.init_with_dicts(24, [
    dict(n1=0, p1=0, n2=1, p2=1),
    dict(n1=0, p1=1, n2=3, p2=1),
    dict(n1=0, p1=2, n2=2, p2=0),

    dict(n1=1, p1=2, n2=2, p2=1),
    dict(n1=1, p1=0, n2=3, p2=3),

    dict(n1=2, p1=2, n2=3, p2=0),

    dict(n1=3, p1=2, n2=4, p2=1),
    dict(n1=3, p1=4, n2=5, p2=3),
    dict(n1=3, p1=6, n2=9, p2=2),
    dict(n1=3, p1=5, n2=8, p2=0),

    dict(n1=4, p1=0, n2=5, p2=1),
    dict(n1=4, p1=3, n2=9, p2=1),
    dict(n1=4, p1=2, n2=8, p2=1),

    dict(n1=5, p1=2, n2=6, p2=0),
    dict(n1=5, p1=4, n2=7, p2=0),
    dict(n1=5, p1=0, n2=8, p2=2),
    dict(n1=5, p1=5, n2=9, p2=0),

    dict(n1=6, p1=1, n2=7, p2=1),

    dict(n1=8, p1=3, n2=9, p2=4),

    dict(n1=9, p1=5, n2=10, p2=0),
    dict(n1=9, p1=6, n2=11, p2=3),

    dict(n1=10, p1=1, n2=11, p2=0),

    dict(n1=11, p1=2, n2=12, p2=0),
    dict(n1=11, p1=4, n2=13, p2=2),
    dict(n1=11, p1=1, n2=16, p2=0),

    dict(n1=13, p1=0, n2=14, p2=0),
    dict(n1=13, p1=1, n2=15, p2=0),

    dict(n1=14, p1=1, n2=15, p2=1),

    dict(n1=16, p1=2, n2=17, p2=1),
    dict(n1=16, p1=1, n2=20, p2=3),

    dict(n1=17, p1=2, n2=18, p2=0),
    dict(n1=17, p1=0, n2=19, p2=0),

    dict(n1=20, p1=2, n2=21, p2=1),
    dict(n1=20, p1=0, n2=22, p2=2),
    dict(n1=20, p1=1, n2=23, p2=1),

    dict(n1=21, p1=0, n2=22, p2=0),
    dict(n1=21, p1=2, n2=23, p2=2),

    dict(n1=22, p1=1, n2=23, p2=0)
])

robot_pos = 0

instance_oracle = Oracle(INSTANCE_ORACLE, Graph)
instance_oracle.encode(robot_pos)
pos = {
    0  : ( 20, 100),
    1  : ( 20, 000),
    2  : (100, 000),
    3  : (100, 100),
    4  : ( 80, 200),
    5  : (150, 250),
    6  : (100, 350),
    7  : (200, 350),
    8  : (200, 100),
    9  : (220, 200),
    10 : (300, 300),
    11 : (350, 200),
    12 : (400, 300),
    13 : (350, 100),
    14 : (300, 000),
    15 : (400, 000),
    16 : (400, 200),
    17 : (450, 150),
    18 : (430,  50),
    19 : (500, 160),
    20 : (450, 250),
    21 : (450, 350),
    22 : (530, 350),
    23 : (530, 250)
}
instance_oracle.print_encoding_info(0)
print(instance_oracle.encode(0))
instance_oracle.encode_with_plotting(robot_pos, pos)

