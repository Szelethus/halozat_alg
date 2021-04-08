import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from Node import Graph, Node, Port, MAP_ORACLE, INSTANCE_ORACLE
from pprint import pprint
from collections import defaultdict


# https://stackoverflow.com/questions/57095809/networkx-connecting-nodes-using-ports

routers = [
    dict( name  = 0, ports = [0, 1, 2] ),
    dict( name  = 1, ports = [0] ),
    dict( name  = 2, ports = [0, 1] ),
    dict( name  = 3, ports = [0] ),
    dict( name  = 4, ports = [0] )
]

G = nx.Graph()

for r in routers:
  # Add ports as attributes
  G.add_node(r['name'], name=r['name'], ports=r['ports'])

G.nodes().get('R3', None)

# Sanity check to see if the nodes and ports are present in Graph
def verify_nodes_and_ports(G, node, port):
    if G.nodes().get(node, None) is None:
        print("Node : {} is not present in Graph".format(node))
        return False

    if G.nodes(data=True)[node]['ports'][port] is None:
        print("Port ID :{} is incorrect for Node ID : {}!".
              format(node, port))
    return False

    return True


def add_edge_port(G, node1, port1, node2, port2):
    verify_nodes_and_ports(G, node1, port1)
    verify_nodes_and_ports(G, node2, port2)

    # Add the anchor points as edge attributes
    G.add_edge(node1, node2, p1=port1, p2=port2)

add_edge_port(G, 0, 2, 0, 0)
add_edge_port(G, 0, 0, 4, 0)
add_edge_port(G, 0, 1, 2, 0)
add_edge_port(G, 2, 1, 3, 0)

print(G.edges(0, data=True))
#print(nx.get_edge_attributes(G, 'anchors'))
