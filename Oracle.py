import math
import pygame
import networkx as nx
import pylab
from pygame.locals import *
import time
import random
from PortNumberedGraph import PortNumberedGraph

MAP_ORACLE = 0
INSTANCE_ORACLE = 1

def get_binary(x, n=0):
    return format(x, 'b').zfill(n)

class Oracle:
    def __init__(self, oracle_type, port_numbered_graph):
        assert oracle_type == MAP_ORACLE or oracle_type == INSTANCE_ORACLE, "Unknown oracle type!"
        self.oracle_type = oracle_type
        self.G = port_numbered_graph
        return

    def verify_nodes_and_ports(self, node, port):
        if self.G.nodes().get(node, None) is None:
            print("Node : {} is not present in Graph".format(node))
            return False

        if port not in self.G.nodes(data=True)[node]['ports']:
            print("Port ID : {} is incorrect for Node ID : {}!".
                  format(port, node))
        return False

        return True

    def encode_with_stats(self, robot_pos):
        spanning_tree = nx.minimum_spanning_tree(self.G)

        if self.oracle_type == INSTANCE_ORACLE:
            edges = nx.dfs_labeled_edges(spanning_tree, robot_pos)
        else:
            # Lets not make it random, otherwise it wouldn't be deterministic
            edges = nx.dfs_labeled_edges(spanning_tree, 0)

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
        encoded_route = str(self.oracle_type) + ''.join(str(x) for x in path + [0] + ports)

        return RobotStatistics(encoded_route, path, node_path, ports, ports_decimal, spanning_tree)

    def encode(self, robot_pos):
        encoded_route, _, _, _, _, _ = self.encode_with_stats(robot_pos)
        return encoded_route

    def print_encoding_info(self, robot_pos):
        encoded_route, path, node_path, ports, ports_decimal, _ = self.encode_with_stats(robot_pos)

        print('---=== Encoding for', 'Map oracle' if self.oracle_type == MAP_ORACLE else 'Instance oracle', ', robot starting position at node', robot_pos, '===---')
        print('Code generated for graph: ', encoded_route)
        print('Structure of the graph (1:forward, 0:reverse): ', path)
        print('DFS sequence of nodes: ', node_path)
        print('DFS sequence of ports: ', ports)
        print('DFS sequence of ports in decimal: ', ports_decimal)
