import networkx as nx
from networkx import minimum_spanning_tree
import math
import pygame
import plot
import pylab
from pygame.locals import *
import time

MAP_ORACLE = 0
INSTANCE_ORACLE = 1

def get_binary(x, n=0):
    return format(x, 'b').zfill(n)

class Graph:
    def __init__(self):
        self.reset()

    def reset(self):
        self.path = []
        self.node_path = []
        self.ports = []
        self.ports_decimal = []

    def init_with_dicts(self, node_count, edges_with_ports):
        self.G = nx.Graph()

        # https://stackoverflow.com/questions/57095809/networkx-connecting-nodes-using-ports
    
        # Initialize the graph with the nodes having only a single port.
        # (the graph must be connected, so each node must have at least one
        # edge, tho verification of the connectivity would be nice)
        for i in range(0, node_count):
            self.G.add_node(i, ports=[0])
    
        # Count how many ports each of the nodes have by inspecting the edge list.
        idx = 0
        while idx < len(edges_with_ports):
            current_edge_count = 0
            current_node = edges_with_ports[idx]['n1']
            while idx < len(edges_with_ports) and edges_with_ports[idx]['n1'] == current_node:
                current_edge_count = current_edge_count + 1
                idx = idx + 1
                self.G.nodes(data=True)[current_node]['ports'].append(current_edge_count)
    
        # Connect these ports with edges.
        for e in edges_with_ports:
            self.add_edge_port(e['n1'], e['p1'], e['n2'], e['p2'])
    
    def verify_nodes_and_ports(self, node, port):
        if self.G.nodes().get(node, None) is None:
            print("Node : {} is not present in Graph".format(node))
            return False
    
        if port not in self.G.nodes(data=True)[node]['ports']:
            print("Port ID : {} is incorrect for Node ID : {}!".
                  format(port, node))
        return False
    
        return True
    
    
    # Connect two nodes on their ports with an edge. Port numbers are added as
    # edge attributes.
    # The query of edge attributes may be done as such:
    #   self.G.get_edge_data(from, to)
    # Which is equivalent to this:
    #   self.G.get_edge_data(to, from)
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
        
        self.G.add_edge(node1, node2, n1=node1, p1=port1, n2=node2, p2=port2)

    # See comments for add_edge_port().
    def get_port_to(self, from_, to):
        data = self.G.get_edge_data(from_, to)
        if (data['n1'] == from_):
            return data['p1']
        else:
            return data['p2']

    def encode(self, oracle_type, robot_pos):
        if oracle_type == INSTANCE_ORACLE:
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), robot_pos)
        else:
            # Lets not make it random, otherwise it wouldn't be deterministic
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), 1)

        self.reset()
        visited_nodes = 0
        bit = math.ceil(math.log(self.G.number_of_nodes(), 2))
        for u, v, d in edges:
            if u == v:
                continue
            if visited_nodes != self.G.number_of_nodes():
                if d == "forward":
                    self.path.append(1)
                    self.node_path.append(u)
                    visited_nodes += 1
                    self.ports.append(get_binary(self.get_port_to(u, v), bit))
                    self.ports_decimal.append(self.get_port_to(u, v))
                elif d == 'reverse':
                    self.path.append(0)
                    self.node_path.append(v)
                    self.ports.append(get_binary(self.get_port_to(v, u), bit))
                    self.ports_decimal.append(self.get_port_to(v, u))
        return ''.join(str(x) for x in self.path + [0] + self.ports)

    # Find the bit deparating the structure of the graph and the port numbers.
    #
    # <structure of the graph>0<port numbers>
    #                          ^~~~~~~~~~~~~~~first return value points to the
    #                                         first bit of the first port
    def get_code_halfway_point(self, code):
        depth = 0
        idx = 0
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
        self.G = nx.Graph()

        halfway_point, node_count = self.get_code_halfway_point(code)
        port_length = math.ceil(math.log(node_count, 2)) 

        structure_idx = 0
        port_idx = halfway_point

        self.G = nx.Graph()

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
            port_word = code[port_idx : port_idx + port_length]
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

                self.add_edge_port_dont_verify_port2(current_node, port, new_node, 'MISSING')

                parents.append(current_node)
                current_node = new_node

        assert port_idx == len(code), "Failed to read port numbers! Faulty code?"

    def print_graph(self):
        print(self.G.edges(data=True))

    def print_encoding_info(self):
        print('Structure of the graph (1:forward, 0:reverse): ', self.path)
        print('DFS sequence of nodes: ', self.node_path)
        print('DFS sequence of ports: ', self.ports)
        print('DFS sequence of ports in decimal: ', self.ports_decimal)

    def get_edge_labels(self):
        edge_labels = {}
        for node1, node2, data in self.G.edges.data():
                edge_labels[(node1, node2)] = (data['p1'], data['p2'])

        formatted_edge_labels = {(elem[0],elem[1]): edge_labels[elem] for elem in edge_labels} # use this to modify the tuple keyed dict if it has > 2 elements, else ignore
        
        return formatted_edge_labels

    def get_map_oracle_f_tours(self):
        f_tours = []

        for root in self.G.nodes():
            ports = []
            visited_nodes = 0
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), root)
            for u, v, d in edges:
                if u == v:
                    continue
                if visited_nodes != self.G.number_of_nodes():
                    if d == "forward":
                        visited_nodes += 1
                        ports.append(self.get_port_to(u, v))
                        ports.append(self.get_port_to(v, u))
                    elif d == 'reverse':
                        ports.append(self.get_port_to(v, u))
                        ports.append(self.get_port_to(u, v))
            print(ports + ports[::-1])
            f_tours.append(ports + ports[::-1]) #euler tour + reverse euler tour with the in,out ports of the edges
        return f_tours
    
    def encode_with_plotting(self, oracle_type, robot_pos, pos):
        if oracle_type == INSTANCE_ORACLE:
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), robot_pos)
        else:
            # Lets not make it random, otherwise it wouldn't be deterministic
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), 1)

        self.reset()
        visited_nodes = 0
        bit = math.ceil(math.log(self.G.number_of_nodes(), 2))

        pygame.init()
        fig = pylab.figure(figsize=[16, 8], dpi=100)
        window = pygame.display.set_mode((1600, 800), DOUBLEBUF)
        screen = pygame.display.get_surface()
        running = True
        plot.initialize_colors(self.G)
        while running:
            # if the user wants to close the window after the algorithm is finished
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            for u, v, d in edges:
                        # if the user wants to close the window during the algorithm is running
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                if running == False:
                    pygame.quit()

                # color only the currently used edge
                plot.clear_edge_colors(self.G)

                if u == v:
                    continue
                if visited_nodes != self.G.number_of_nodes():
                    if d == "forward":
                        self.path.append(1)
                        self.node_path.append(u)
                        visited_nodes += 1
                        self.ports.append(get_binary(self.get_port_to(u, v), bit))
                        self.ports_decimal.append(self.get_port_to(u, v))
                        plot.color_forward_edge(self.G, u, v)
                    elif d == 'reverse':
                        self.path.append(0)
                        self.node_path.append(v)
                        self.ports.append(get_binary(self.get_port_to(v, u), bit))
                        self.ports_decimal.append(self.get_port_to(v, u))
                        plot.color_reverse_edge(self.G, v, u)
                    else:
                        continue
                
                plot.draw_window(self.G, screen, fig, self, pos)
                
                pygame.display.flip()
                time.sleep(0.3)
            #running = False

            plot.clear_edge_colors(self.G)
            plot.draw_window(self.G, screen, fig, self, pos)
            pygame.display.flip()

        #pygame.quit()

        return ''.join(str(x) for x in self.path + [0] + self.ports)

        def map_oracle_with_plotting(self):
            pygame.init()
            fig = pylab.figure(figsize=[7, 5], dpi=100)
            window = pygame.display.set_mode((700, 500), DOUBLEBUF)
            screen = pygame.display.get_surface()
            running = True
            while running:
                # if the user wants to close the window after the algorithm is finished
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                f_tours = []
                plot.initialize_colors(self.G)
                for root in self.G.nodes():
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    if running == False:
                        pygame.quit()

                

                    ports = []
                    visited_nodes = 0
                    edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), root)
                    for u, v, d in edges:
                        # color only the currently used edge
                        plot.clear_edge_colors(self.G)
                        if u == v:
                            continue
                        if visited_nodes != self.G.number_of_nodes():
                            if d == "forward":
                                visited_nodes += 1
                                ports.append(self.get_port_to(u, v))
                                ports.append(self.get_port_to(v, u))
                            elif d == 'reverse':
                                ports.append(self.get_port_to(v, u))
                                ports.append(self.get_port_to(u, v))

                        plot.draw_window(self.G, screen, fig, self)
                
                        pygame.display.flip()
                        time.sleep(1)
                    print(ports + ports[::-1])
                    f_tours.append(ports + ports[::-1]) #euler tour + reverse euler tour with the in,out ports of the edges

                plot.clear_edge_colors(self.G)
                plot.draw_window(self.G, screen, fig, self)
                pygame.display.flip()
            pygame.quit()

            return f_tours
