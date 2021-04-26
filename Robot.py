import math
import pygame
import pylab
from pygame.locals import *
import time
import random
import networkx as nx
from PortNumberedGraph import PortNumberedGraph
from Oracle import MAP_ORACLE, INSTANCE_ORACLE
from Statistics import ExplorationStatistics

class PathExploration:
    def __init__(self, original_graph, starting_pos, f_tour):
        # A list of tuples describing the ports the robot has taken so far in
        # the following structure:
        #   (node_from, node_to, port, direction)
        # Where the
        #   * port is the port to be taken from node_from to reach node_to
        #   * direction is one of the following:
        #     - forward
        #     - reverse
        #     - backtrack, if the exploration failed and the robot is in the 
        #     process of going back to its starting point.
        self.edge_exploration_sequence = []

        # A list of port numbers to be followed in a reverse order to reach the
        # starting point.
        self.backtrack = []

        # The original graph -- NOT what the robot has constructed for itself.
        # The robot is unaware of the original graph; this class is unaware of
        # what the robot has constructed.
        self.original_graph = original_graph

        # Mind that the robot doesn't know its position in the graph! From its
        # perspective, only port numbers exist.
        self.current_node = starting_pos
        self.starting_pos = starting_pos

        self.robot_root_id = f_tour[0]
        self.port_sequence = f_tour[1]

    # From its current position, try to make the robot go through a port.
    # Returns false if no such port exists at the current position.
    def try_take_port(self, port, reverse_kind = 'reverse'):
        to = self.original_graph.get_destination_of_port(self.current_node, port)
        if (to == -1):
            return False

        # The port we'd need to take from the 'to' node to get back to
        # 'self.current_node'.
        backtrack_port = self.original_graph.get_port_to(to, self.current_node)

        # If we're going back to the previous node, we can pop the backtrack
        # stack.
        if len(self.backtrack) > 0 and port == self.backtrack[-1]:
            self.edge_exploration_sequence.append((self.current_node, to, port, reverse_kind))
            self.current_node = to
            self.backtrack.pop()
        else:
            self.edge_exploration_sequence.append((self.current_node, to, port, 'forward'))
            self.current_node = to
            self.backtrack.append(backtrack_port)

        return True

    def track_back_to_start(self):
        while len(self.backtrack) > 0:
            port = self.backtrack[-1]
            if not self.try_take_port(port, 'backtrack'):
                assert False, "Failed to track back to start!"

    def try_to_explore(self):
        assert self.edge_exploration_sequence == [], "Path exploration is already complete!"

        for port in self.port_sequence:
            if not self.try_take_port(port):
                #print('Cannot proceed from node {} through port {}'.format(self.current_node, port))
                self.track_back_to_start()
                break
        return ExplorationStatistics(self.robot_root_id, self.starting_pos, self.port_sequence, self.edge_exploration_sequence)

class Robot:
    def __init__(self, code):
        self.init_with_decode(code)

    # Find the bit deparating the structure of the graph and the port numbers.
    #
    # <structure of the graph>0<port numbers>
    #                          ^~~~~~~~~~~~~~~first return value points to the
    #                                         first bit of the first port
    def get_code_halfway_point(self, code):
        depth = 0
        # 0th index os the oracle type indicator.
        idx = 1
        node_count = 1

        while idx < len(code):
            c = code[idx]
            idx = idx + 1

            # We finished parsing the structure of the graph.
            if depth == 0 and c == '0':
                break;
            # 0 means "go up in the tree".
            elif c == '0':
                depth = depth - 1
            # 1 means "go down in the tree" (to an unvisited node).
            else:
                depth = depth + 1
                node_count = node_count + 1

        return idx, node_count

    def init_with_decode(self, code):
        self.G = PortNumberedGraph()

        halfway_point, node_count = self.get_code_halfway_point(code)
        port_length = math.ceil(math.log(node_count, 2))

        # 0th index os the oracle type indicator.
        self.oracle_type = int(code[0])
        structure_idx = 1
        port_idx = halfway_point

        # Add a root.
        self.G.add_node(0, ports=[])
        current_node = 0

        # Parent stack. Last element is the parent of the current node, the one
        # before that is the parent of the last element, and so on.
        parents = []

        self.instance_oracle_tour = []

        while structure_idx < halfway_point - 1:
            structure_bit = code[structure_idx]
            structure_idx = structure_idx + 1

            # Port numbers will be assigned such that 'p1' will be the port
            # "going down", and 'p2' the port "going up".
            port_word = code[port_idx: port_idx + port_length]
            port = int(port_word, 2)
            self.instance_oracle_tour.append(port)
            port_idx = port_idx + port_length

            # We finished parsing the structure of the graph. This can only
            # occur if we reached the halfway point, in which case we should not
            # have entered another iteration, or if we messed up something.
            assert current_node != 0 or structure_bit != '0'

            # 0 means "go up in the tree".
            if structure_bit == '0':
                next_node = parents.pop()
                self.G.get_edge_data(next_node, current_node)['p2'] = port
                current_node = next_node

            # 1 means "go down in the tree" (to an unvisited node).
            else:
                new_node = self.G.number_of_nodes()
                self.G.add_node(new_node, ports=[0])
                self.G.nodes(data=True)[current_node]['ports'].append(port)

                self.G.add_edge_port_dont_verify_port2(current_node, port, new_node, 'MISSING')

                parents.append(current_node)
                current_node = new_node

        assert port_idx == len(code), "Failed to read port numbers! Faulty code?"
        assert nx.is_tree(self.G), "Failed to construct a tree out of the code!"

    def traverse(self, original_graph, starting_pos):
        if self.oracle_type == INSTANCE_ORACLE:
            return self.traverse_instance_oracle(original_graph, starting_pos)
        else:
            f_tours = self.get_map_oracle_f_tours()
            return self.traverse_map_oracle(original_graph, starting_pos, f_tours)

    def traverse_instance_oracle(self, original_graph, starting_pos):
        assert self.oracle_type == INSTANCE_ORACLE
        explored_ports = PathExploration(original_graph, starting_pos)

        if not explored_ports.try_explore_port_sequence(self.instance_oracle_tour):
            assert False, "Failed to explore the graph with a instane oracle advice!"
        return explored_ports
        
    def get_map_oracle_f_tours(self):
        assert self.oracle_type == MAP_ORACLE
        f_tours = []

        for root in self.G.nodes():
            ports = []
            ports_reverse = []
            visited_nodes = 0
            edges = nx.dfs_labeled_edges(nx.minimum_spanning_tree(self.G), root)
            for u, v, d in edges:
                if u == v:
                    continue
                if visited_nodes != self.G.number_of_nodes():
                    if d == "forward":
                        visited_nodes += 1
                        ports.append(self.G.get_port_to(u, v))
                        ports_reverse.append(self.G.get_port_to(v, u))
                    elif d == 'reverse':
                        ports.append(self.G.get_port_to(v, u))
                        ports_reverse.append(self.G.get_port_to(u, v))
            # Root + f tour
            f_tours.append((root, ports + ports_reverse[::-1]))
        return f_tours

    def traverse_map_oracle(self, original_graph, starting_pos, f_tours):
        assert self.oracle_type == MAP_ORACLE
        
        stats_collection = []

        was_exploration_successful = False

        for tour in f_tours:
            explored_ports = PathExploration(original_graph, starting_pos, tour)
            stats = explored_ports.try_to_explore()
            stats_collection.append(stats)
            if stats.was_exploration_successful():
                was_exploration_successful = True

        print('starting pos:', starting_pos)
        assert was_exploration_successful, "Failed to explore the graph with a map oracle advice!"
        return stats_collection
