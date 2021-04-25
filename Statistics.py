import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from PortNumberedGraph import PortNumberedGraph
from Oracle import Oracle, MAP_ORACLE, INSTANCE_ORACLE
from Robot import Robot
from Plot import Plot
from GraphGenerator import GraphGenerator

class GraphStatistics:
    def __init__(self, Graph, note):
        self.G = Graph
        self.note = note

    def get_edge_count(self):
        return len(self.G.edges)

    def get_node_count(self):
        return len(self.G.nodes)

    def get_graph_density(self):
        return self.get_edge_count() / self.get_node_count()

class TreeStatistics(GraphStatistics):
    def __init__(self, Graph, note, root_id):
        GraphStatistics.__init__(Graph, note)
        self.root_id = root_id

    def get_leaf_count(self):
        return len([x for x in G.nodes() if G.out_degree(x)==0 and G.in_degree(x)==1])

    def get_number_of_different_edges(self):
        nontree = 0
        reverse = 0
        forward = 0
        for u,v, d in edges:
            if d == "forward":
                forward = forward + 1
            elif d == "reverse":
                reverse = reverse + 1
            elif d == "nontree":
                nontree = nontree + 1
        return forward, reverse, nontree

class OracleStatistics:
    def __init__(self, original_graph_stats, spanning_tree_stats, path, node_path, tree_node_expl_order, ports, ports_decimal, code):
        self.original_graph_stats = original_graph_stats
        self.spanning_tree_stats = spanning_tree_stats
        self.path = path
        self.node_path = node_path
        self.tree_node_expl_order = tree_node_expl_order
        self.ports = ports
        self.ports_decimal = ports_decimal
        self.code = code
    
    def get_code_length():
        return len(self.code)

class RobotStatistics:
    def __init__(self, ):

