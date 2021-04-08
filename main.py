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

r1 = dict( name  = 'R1', ports = [0, 1] )
r2 = dict( name  = 'R2', ports = [0, 1] )
r3 = dict( name  = 'R3', ports = [0, 1] )

routers = [r1,r2,r3]

G = nx.Graph()

for r in routers:
  # Add ports as attributes
  G.add_node(r['name'], name=r['name'], ports=r['ports'])

G.nodes().get('R3', None)

def add_edge_port(G, node1, port1, node2, port2):
  node_list = [node1, node2]
  port_list = [port1, port2]

  edge_ports = []

  for idx in range(0, 2):
    node_idx = node_list[idx]
    port_idx = port_list[idx]

    # Sanity check to see if the nodes and ports are present in Graph
    if G.nodes().get(node_idx, None) is None:
      print("Node : {} is not present in Graph".format(node_idx))
      return

    if G.nodes(data=True)[node_idx]['ports'][port_idx] is None:
      print("Port ID :{} is incorrect for Node ID : {}!".
            format(node_idx, port_idx))
      return

    edge_ports.append(node_idx + '.' + str(port_idx))

  # Add the anchor points as edge attributes
  G.add_edge(node1, node2, anchors=edge_ports)

add_edge_port(G, 'R1', 1, 'R2', 0)
print(nx.get_edge_attributes(G, 'anchors'))
