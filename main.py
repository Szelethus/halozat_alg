import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from Node import Graph, Node, Port, MAP_ORACLE, INSTANCE_ORACLE
from pprint import pprint
from collections import defaultdict


# https://stackoverflow.com/questions/57095809/networkx-connecting-nodes-using-ports

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

    G.add_edge(node1, node2, p1=port1, p2=port2)

def construct_graph(node_count, edges_with_ports):
    G = nx.Graph()

    # Initialize the graph with the nodes with only a single port.
    # (the graph must be connected, so this this is okay, tho verification would
    # be nice)
    for i in range(0, node_count):
        G.add_node(i, ports=[0])

    # Count how many ports each of the nodes have by inspecting the edge list.
    idx = 0
    while idx < len(edges_with_ports):
        current_edge_count = 0
        current_node = edges_with_ports[idx]['n1']
        while idx < len(edges_with_ports) and edges_with_ports[idx]['n1'] == current_node:
            current_edge_count = current_edge_count + 1
            idx = idx + 1
            G.nodes(data=True)[current_node]['ports'].append(current_edge_count)

    # Connect these ports with edges.
    for e in edges_with_ports:
        add_edge_port(G, e['n1'], e['p1'], e['n2'], e['p2'])

    return G

G = construct_graph(5, [
    dict(n1=0, p1=2, n2=0, p2=0),
    dict(n1=0, p1=0, n2=4, p2=0),
    dict(n1=0, p1=1, n2=2, p2=0),
    dict(n1=2, p1=1, n2=3, p2=0)
])

# List the edges connected to node 0:
print(G.edges(0, data=True))
