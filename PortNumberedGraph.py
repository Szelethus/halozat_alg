import networkx as nx
from networkx import minimum_spanning_tree
import math
import pygame
import Plot
import pylab
from pygame.locals import *
import time

class PortNumberedGraph(nx.Graph):
    def init_with_dicts(self, node_count, edges_with_ports):
        # https://stackoverflow.com/questions/57095809/networkx-connecting-nodes-using-ports

        # Initialize the graph with the nodes having only a single port.
        # (the graph must be connected, so each node must have at least one
        # edge, tho verification of the connectivity would be nice)
        for i in range(0, node_count):
            self.add_node(i, ports=[0])

        # Count how many ports each of the nodes have by inspecting the edge list.
        for edge_info in edges_with_ports:
            ports = self.nodes(data=True)[edge_info['n1']]['ports']
            ports.append(ports[-1] + 1)
            ports = self.nodes(data=True)[edge_info['n2']]['ports']
            ports.append(ports[-1] + 1)

        self.print_graph()
        # Connect these ports with edges.
        for e in edges_with_ports:
            self.add_edge_port(e['n1'], e['p1'], e['n2'], e['p2'])

    def verify_nodes_and_ports(self, node, port):
        if self.nodes().get(node, None) is None:
            raise Exception("Node : {} is not present in Graph".format(node))
            return False
        if port not in self.nodes(data=True)[node]['ports']:
            raise Exception("Node {} does not have port ID {}!".
                  format(node, port))
        return False

        return True

    # Connect two nodes on their ports with an edge. Port numbers are added as
    # edge attributes.
    # The query of edge attributes may be done as such:
    #   self.get_edge_data(from, to)
    # Which is equivalent to this:
    #   self.get_edge_data(to, from)
    # Port numbers are however not interchangable, and this makes it impossible
    # to know whether 'p1' belongs to the 'to' node or the 'from' node; as such,
    # the following tuple serves as edge attributes:
    #   node1, port1, node2, port2
    def add_edge_port(self, node1, port1, node2, port2):
        self.verify_nodes_and_ports(node2, port2)
        self.add_edge_port_dont_verify_port2(node1, port1, node2, port2)

    # The port number during decoding is supplied such that we recieve the port
    # "on the way down", and the one "on the way back" a bit later. As such,
    # the second port will be missing.
    def add_edge_port_dont_verify_port2(self, node1, port1, node2, port2):
        self.verify_nodes_and_ports(node1, port1)

        self.add_edge(node1, node2, n1=node1, p1=port1, n2=node2, p2=port2)

    # See comments for add_edge_port().
    def get_port_to(self, from_, to):
        data = self.get_edge_data(from_, to)
        if (data['n1'] == from_):
            return data['p1']
        else:
            return data['p2']

    def get_destination_of_port(self, from_, port):
        for edge in self.edges(data=True):
            if edge['n1'] == from_ and edge['p1'] == port:
                return edge['n2']
            elif edge['n2'] == from_ and edge['p2'] == port:
                return edge['n1']
        return -1

    def print_graph(self):
        print('Nodes', self.nodes(data=True))
        print('Edges', self.edges(data=True))

    def get_edge_labels(self):
        edge_labels = {}
        for node1, node2, data in self.edges.data():
            edge_labels[(node1, node2)] = (data['p1'], data['p2'])

        formatted_edge_labels = {(elem[0], elem[1]): edge_labels[elem] for elem in
                                 edge_labels}  # use this to modify the tuple keyed dict if it has > 2 elements, else ignore

        return formatted_edge_labels

    def quick_display_graph(self):
        pygame.init()
        fig = pylab.figure(figsize=[16, 8], dpi=100)
        window = pygame.display.set_mode((1600, 800), DOUBLEBUF)
        screen = pygame.display.get_surface()
        plot.initialize_colors(self)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            plot.draw_window(self, screen, fig, self, None)
            pygame.display.flip()
    
    def find_edge(self, p1, p2, robot_pos):
        i = 0
        for u, v, edge in self.edges.data(True):
            if robot_pos == u:
                if self.get_port_to(u, v) == p1 and (edge['p1'] == p2 or edge['p2'] == p2):
                    return u, v
            elif robot_pos == v:
                if self.get_port_to(v, u) == p1 and (edge['p1'] == p2 or edge['p2'] == p2):
                    return u, v

            i += 1
        if i == len(self.edges):
            return i, i
