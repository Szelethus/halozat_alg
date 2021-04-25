import math
import pygame
import networkx as nx
import pylab
from pygame.locals import *
import time
import random
from PortNumberedGraph import PortNumberedGraph
from Statistics import OracleStatistics

MAP_ORACLE = 0
INSTANCE_ORACLE = 1

def get_binary(x, n=0):
    return format(x, 'b').zfill(n)

class Oracle:
    def __init__(self, port_numbered_graph):
        self.G = port_numbered_graph

    def verify_nodes_and_ports(self, node, port):
        if self.G.nodes().get(node, None) is None:
            print("Node : {} is not present in Graph".format(node))
            return False

        if port not in self.G.nodes(data=True)[node]['ports']:
            print("Port ID : {} is incorrect for Node ID : {}!".
                  format(port, node))
        return False

        return True

    def get_oracle_bit(self):
        assert False

    def encode_with_stats(self):
        spanning_tree = nx.minimum_spanning_tree(self.G)
        edges = nx.dfs_labeled_edges(spanning_tree, self.root_id)

        path = []
        node_path = []
        tree_node_expl_order = []
        ports = []
        ports_decimal = []

        visited_nodes = 0
        bit = math.ceil(math.log(self.G.number_of_nodes(), 2))
        for u, v, d in edges:
            if u == v:
                continue
            if visited_nodes != self.G.number_of_nodes():
                if d == "forward":
                    #print('going from node', u, 'to', v, 'in', d)
                    path.append(1)
                    node_path.append(v)
                    tree_node_expl_order.append(v)
                    visited_nodes += 1
                    ports.append(get_binary(self.G.get_port_to(u, v), bit))
                    ports_decimal.append(self.G.get_port_to(u, v))
                elif d == 'reverse':
                    #print('going from node', v, 'to', u, 'in', d)
                    path.append(0)
                    node_path.append(u)
                    ports.append(get_binary(self.G.get_port_to(v, u), bit))
                    ports_decimal.append(self.G.get_port_to(v, u))
        encoded_route = str(self.get_oracle_bit()) + ''.join(str(x) for x in path + [0] + ports)

        return OracleStatistics(self.get_oracle_bit(), self.G, spanning_tree, \
                                self.root_id, path, node_path, tree_node_expl_order, \
                                ports, ports_decimal, encoded_route)

    def encode(self):
        return self.encode_with_stats().code

    def print_encoding_info(self):
        stats = self.encode_with_stats()

        print('---=== Encoding for', 'Map oracle' if self.get_oracle_bit() == MAP_ORACLE else 'Instance oracle ===---')
        print('Code generated for graph: ', stats.code)
        print('Structure of the graph (1:forward, 0:reverse): ', stats.path)
        print('DFS sequence of nodes: ', stats.node_path)
        print('DFS sequence of ports: ', stats.ports)
        print('DFS sequence of ports in decimal: ', stats.ports_decimal)

class MapOracle(Oracle):
    def __init__(self, port_numbered_graph):
        super().__init__(port_numbered_graph)
        self.root_id = 0

    def get_oracle_bit(self):
        return MAP_ORACLE

class InstanceOracle(Oracle):
    def __init__(self, port_numbered_graph, starting_pos):
        super().__init__(port_numbered_graph)
        self.root_id = starting_pos

    def get_oracle_bit(self):
        return INSTANCE_ORACLE
