import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from PortNumberedGraph import PortNumberedGraph
from Plot import Plot
from GraphGenerator import GraphGenerator

class OracleStatistics:
    def __init__(self, oracle_type, original_graph, spanning_tree, root_id, path, node_path,\
                 tree_node_expl_order, ports, ports_decimal, code):

        self.oracle_type = oracle_type
        self.original_graph = original_graph
        self.spanning_tree = spanning_tree
        self.root_id = root_id
        self.path = path
        self.node_path = node_path
        self.tree_node_expl_order = tree_node_expl_order
        self.ports = ports
        self.ports_decimal = ports_decimal
        self.code = code
    
    def get_code_length():
        return len(self.code)

class RobotStatistics:
    def __init__(self):
        return

