import math
import pygame
from Plot import Plot
import pylab
from pygame.locals import *
import time
import random
import networkx as nx
from PortNumberedGraph import PortNumberedGraph
from Oracle import MAP_ORACLE, INSTANCE_ORACLE

class Robot:
    # TODO: We should construct our own graph, but traverse the original.
    def __init__(self, code, original_graph, starting_pos):
        self.init_with_decode(code)
        self.original_graph = original_graph
        self.current_node = starting_pos

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

        while structure_idx < halfway_point - 1:
            structure_bit = code[structure_idx]
            structure_idx = structure_idx + 1

            # Port numbers will be assigned such that 'p1' will be the port
            # "going down", and 'p2' the port "going up".
            port_word = code[port_idx: port_idx + port_length]
            port = int(port_word, 2)
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

    def traverse(self):
        if self.oracle_type == INSTANCE_ORACLE:
            self.traverse_instance_oracle
        else:
            f_tours = self.get_map_oracle_f_tours()
            self.map_oracle_robot(f_tours)

    def traverse_instance_oracle(self):
        assert self.oracle_type == INSTANCE_ORACLE
        steps = []
        

    def get_map_oracle_f_tours(self):
        assert self.oracle_type == MAP_ORACLE
        f_tours = []

        for root in self.G.nodes():
            ports = []
            visited_nodes = 0
            edges = nx.dfs_labeled_edges(nx.minimum_spanning_tree(self.G), root)
            for u, v, d in edges:
                if u == v:
                    continue
                if visited_nodes != self.G.number_of_nodes():
                    if d == "forward":
                        visited_nodes += 1
                        ports.append(self.G.get_port_to(u, v))
                    elif d == 'reverse':
                        ports.append(self.G.get_port_to(v, u))
            print(ports + ports[::-1])
            f_tours.append(ports + ports[::-1])  # euler tour + reverse euler tour with the in,out ports of the edges
        return f_tours

    def map_oracle_robot(self, f_tours):
        f_tour_idx = 0
        ports_taken = []

        running = True
        found = False
        plot = Plot()
        plot.initialize_colors(self.G)
        while running:
            if plot.has_quit():
               running = False
               break;

            if found == False:
                for tour in f_tours:
                    f_tour_idx = 0
                    for port in tour:
                        if plot.has_quit():
                           running = False
                           break;
                        if running == False:
                            pygame.quit()

                        to = self.G.get_destination_of_port(self.current_node, port)
                        if (to == -1):
                            print('Cannot proceed ')
                            break

                        ports_taken.append(port)

                        # color only the currently used edge
                        plot.clear_edge_colors(self.G)

                        if u == self.current_node:
                            self.current_node = v
                            plot.color_forward_edge(self.G, u, v)
                            print(u, v)
                        elif v == self.current_node:
                            self.current_node = u
                            plot.color_reverse_edge(self.G, v, u)
                            print(v, u)

                        plot.draw_window(self.G, screen, fig, self, fig_pos)

                        pygame.display.flip()
                        time.sleep(0.3)

                        f_tour_idx += 1
                    if f_tour_idx == len(tour):
                        print(tour)
                        print('Found')
                        found = True
                        break
                    else:
                        while len(ports_taken) != 1:
                            plot.clear_edge_colors(self.G)
                            u, v = self.find_edge(ports_taken[-1], ports_taken[-2], self.current_node)
                            plot.color_reverse_edge(self.G, v, u)
                            plot.draw_window(self.G, None)
                            pygame.display.flip()
                            
                        plot.initialize_colors(self.G)


            plot.clear_edge_colors(self.G)
            plot.draw_window(self.G, None)
            pygame.display.flip()
        pygame.quit()
