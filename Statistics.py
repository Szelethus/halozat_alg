import math
import networkx as nx

from PortNumberedGraph import PortNumberedGraph, get_graph_csv_columns
from GraphGenerator import GraphGenerator
import csv_helper

# Comprehensive statistics describing the the ecoding mechanism of the oracle.
class OracleStatistics:
    def __init__(self, oracle_type, original_graph, spanning_tree, root_id, path, node_path,\
                 tree_node_expl_order, ports, ports_decimal, code):

        self.oracle_type = oracle_type
        self.original_graph = original_graph
        # The spanning tree used by oracle, on which the encoding is based.
        self.spanning_tree = spanning_tree
        # The node number on which the spanning tree is rooted.
        self.root_id = root_id
        self.structure = path
        # Node sequence describing the euler route of the DFS exploration
        # in the spanning tree.
        self.node_path = node_path
        # Nodes of the graph in the order of visitation. Nodes are only present
        # once.
        # The robot will construct its tree in this order; for example:
        #   If a graph with 5 nodes are visited in the DFS exploration in the 
        #   following order: [3,2,1,0,4], the robot will reconstruct its graph
        #   with its first node being node 3, its second node is node 2.
        # This field allows us to realize what the robot's graph nodes are in
        # the original graph.
        self.tree_node_expl_order = tree_node_expl_order
        assert len(self.tree_node_expl_order) == len(self.original_graph.nodes())

        self.ports = ports
        self.ports_decimal = ports_decimal
        self.code = code
    
    def get_code_length():
        return len(self.code)

    def get_spanning_tree_edge_kinds(self):
        assert nx.is_tree(self.spanning_tree), "Edge kinds requested on a non-tree graph!"
        nontree = 0
        reverse = 0
        forward = 0
        for u,v, d in nx.dfs_labeled_edges(self.spanning_tree, self.root_id):
            if d == "forward":
                forward = forward + 1
            elif d == "reverse":
                reverse = reverse + 1
            elif d == "nontree":
                nontree = nontree + 1
        return forward, reverse, nontree

    def get_leaf_count(self):
        assert nx.is_tree(self.spanning_tree), "Leaf count requested on a non-tree graph!"
        return sum([1 for node in self.spanning_tree if self.spanning_tree.degree(node)==1])

    def get_csv_data(self):
        forward, reverse, _ = self.get_spanning_tree_edge_kinds()

        return_val = [self.oracle_type, forward, reverse, \
                      self.get_leaf_count(), self.root_id, \
                      self.tree_node_expl_order, self.node_path, \
                      self.ports_decimal]
        
        assert len(get_oracle_csv_columns()) == len(return_val)
        return return_val

def get_oracle_csv_columns():
    return ['oracle type', 'tree forward edges', 'tree reverse edges', \
            'tree leaf count', 'tree root id', 'node visit sequence', \
            'node exploration sequence', 'port encoding']

class ExplorationStatistics:
    def __init__(self, robot_root_id, starting_pos, f_tour, exploration_sequence, expl_time):
        # The root of the route in the graph that the robot constructed. This
        # node ID does NOT describe the same node in the original graph!
        self.robot_root_id = robot_root_id
        # The root of the route in the original graph. The robot doesn't know
        # how the original graph looks like; this will be realized later
        # with the help of an OracleStatistics object.
        self.actual_root_id = None
        self.actual_robot_starting_pos = starting_pos
        self.f_tour = f_tour
        self.exploration_sequence = exploration_sequence
        self.expl_time = expl_time

    def port_sequence(self):
        return [port for _, _, port, _ in self.exploration_sequence]

    def was_exploration_successful(self):
        return self.f_tour == self.port_sequence()

    def get_exploration_kinds(self):
        forward = 0
        reverse = 0
        backtrack = 0
        for _, _, _, direction in self.exploration_sequence:
            if direction == "forward":
                forward += 1
            elif direction == 'reverse':
                reverse += 1
            elif direction == 'backtrack':
                backtrack += 1
            else:
                assert False
        return forward, reverse, backtrack
    
    def realize_actual_root_ids(self, oracle_stats):
        self.actual_root_id = oracle_stats.tree_node_expl_order[self.robot_root_id]

    def get_csv_data(self):
        forward, reverse, backtrack = self.get_exploration_kinds()

        return_val = [self.actual_root_id, self.actual_robot_starting_pos, \
                      self.port_sequence(), len(self.port_sequence()), \
                      forward, reverse, backtrack, \
                      self.was_exploration_successful(), self.expl_time]
        
        assert len(get_exploration_csv_columns()) == len(return_val)
        return return_val

def get_exploration_csv_columns():
    return ['route root', 'robot starting node', 'port sequence', \
            'exploration length', 'forward edges taken', \
            'reverse edges taken', 'backtrack length', 'was route successful', 'time']

class CombinedStatistics:
    def __init__(self, graph, oracle_stats, explorations_stats):
        self.graph = graph
        self.oracle_stats = oracle_stats
        for expl_stat in explorations_stats:
            expl_stat.realize_actual_root_ids(self.oracle_stats)
        self.explorations_stats = explorations_stats

    def fill_csv(self, filename):
        for expl_stat in self.explorations_stats:
            data = self.graph.get_csv_data() + \
                   self.oracle_stats.get_csv_data() + \
                   expl_stat.get_csv_data()
            
            assert len(get_combined_csv_columns()) == len(data)
            csv_helper.write_new_datas(filename, data)

def get_combined_csv_columns():
    return get_graph_csv_columns() + \
           get_oracle_csv_columns() + \
           get_exploration_csv_columns()

