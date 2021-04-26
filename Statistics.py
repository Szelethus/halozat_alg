import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from PortNumberedGraph import PortNumberedGraph
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

class ExplorationStatistics:
    def __init__(self, robot_root_id, f_tour, exploration_sequence):
        self.robot_root_id = robot_root_id
        self.actual_root_id = None
        self.f_tour = f_tour
        self.exploration_sequence = exploration_sequence

    def was_exploration_successful(self):
        return self.f_tour == [port for _, _, port, _ in self.exploration_sequence]

    def get_exploration_kinds(self):
        forward = 0
        reverse = 0
        backtrack = 0
        for from_, to, port_taken, direction in self.explored_ports:
            if direction == "forward":
                forward += 1
            elif direction == 'reverse':
                reverse += 1
            elif direction == 'backtrack':
                backtrack += 1
            else:
                assert False
        return forward, reverse, backward
    
    def realize_actual_root_ids(self, tree_node_expl_order):
        self.actual_root_id = tree_node_expl_order[self.robot_root_id]

class RobotStatistics:
    def __init__(self):
        return

