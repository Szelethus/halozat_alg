import math
import pygame
import plot
import pylab
from pygame.locals import *
import time
import random

MAP_ORACLE = 0
INSTANCE_ORACLE = 1


def get_binary(x, n=0):
    return format(x, 'b').zfill(n)


class Robot:
    def __init__(self):
        return

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
        self.G = PortNumberedGraph.PortNumberedGraph()

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

                self.add_edge_port_dont_verify_port2(current_node, port, new_node, 'MISSING')

                parents.append(current_node)
                current_node = new_node

        assert port_idx == len(code), "Failed to read port numbers! Faulty code?"

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
            f_tours.append(ports + ports[::-1])  # euler tour + reverse euler tour with the in,out ports of the edges
        return f_tours
    def map_oracle_with_plotting(self):
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
            f_tours.append(
                ports + ports[::-1])  # euler tour + reverse euler tour with the in,out ports of the edges

        return f_tours

    def map_oracle_robot(self, f_tours, robot_pos, fig_pos):
        current_node = robot_pos
        i = 0

        pygame.init()
        fig = pylab.figure(figsize=[16, 8], dpi=100)
        window = pygame.display.set_mode((1600, 800), DOUBLEBUF)
        screen = pygame.display.get_surface()
        running = True
        found = False
        plot.initialize_colors(self.G)
        while running:
            # if the user wants to close the window after the algorithm is finished
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if found == False:
                for tour in f_tours:
                    i = 0
                    for k in range(int(len(tour) / 2)):
                        # if the user wants to close the window during the algorithm is running
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                        if running == False:
                            pygame.quit()

                        # color only the currently used edge
                        plot.clear_edge_colors(self.G)

                        u, v = self.find_edge(tour[i], tour[i + 1], current_node)
                        if u == len(self.G.edges):
                            print('Cannot proceed ')
                            current_node = robot_pos
                            plot.initialize_colors(self.G)
                            break
                        elif u == current_node:
                            current_node = v
                            plot.color_forward_edge(self.G, u, v)
                            print(u, v)
                        elif v == current_node:
                            current_node = u
                            plot.color_reverse_edge(self.G, v, u)
                            print(v, u)

                        plot.draw_window(self.G, screen, fig, self, fig_pos)

                        pygame.display.flip()
                        time.sleep(0.3)

                        i += 2
                    if i == len(tour):
                        print(tour)
                        print('Found')
                        found = True
                        break

            plot.clear_edge_colors(self.G)
            plot.draw_window(self.G, screen, fig, self, fig_pos)
            pygame.display.flip()
        pygame.quit()


    def find_edge(self, p1, p2, robot_pos):
        i = 0
        for u, v, edge in self.G.edges.data(True):
            if robot_pos == u:
                if self.get_port_to(u, v) == p1 and (edge['p1'] == p2 or edge['p2'] == p2):
                    return u, v
            elif robot_pos == v:
                if self.get_port_to(v, u) == p1 and (edge['p1'] == p2 or edge['p2'] == p2):
                    return u, v

            i += 1
        if i == len(self.G.edges):
            return i, i

    def get_random_graph(self, number_of_node):
        node_s = []
        port_s = list()
        edge_s = []
        pair_s = []

        # add first n1, p1, n2, p2
        for i in range(number_of_node):
            port_s.insert(i, 0)
        n1 = random.randint(0, number_of_node - 1)
        p1 = 0
        node_s.append(n1)
        n2 = random.randint(0, number_of_node - 1)
        while (n2 == n1):
            n2 = random.randint(0, number_of_node - 1)
        p2 = 0
        node_s.append(n2)
        print(n1, n2, p1, p2)
        pair_s.append([n1, n2])
        edge_s.append([n1, p1, n2, p2])
        # add other n1, p1, n2, p2 in a spanning tree
        for i in range(1, number_of_node - 1):
            n1 = random.choice(node_s)
            p1 = port_s[n1] + 1
            port_s[n1] += 1
            n2 = random.randint(0, number_of_node - 1)
            while n2 in node_s:
                n2 = random.randint(0, number_of_node - 1)
            p2 = 0
            node_s.append(n2)
            print(n1, n2, p1, p2)
            pair_s.append([n1, n2])
            edge_s.append([n1, p1, n2, p2])

        # add extra edges to the tree if you don't just need tree
        '''for i in range(random.randint(0, int((number_of_node * (number_of_node - 1) / 2) - (number_of_node - 1)))):
            n1 = random.randint(0, number_of_node - 1)
            n2 = random.randint(0, number_of_node - 1)
            while [n1, n2] in pair_s or port_s[n1] == number_of_node - 2:
                n1 = random.randint(0, number_of_node - 1)
            p1 = port_s[n1] + 1
            port_s[n1] += 1
            while [n1, n2] in pair_s or [n2, n1] in pair_s or port_s[n2] == number_of_node - 2 or n2 == n1:
                n2 = random.randint(0, number_of_node - 1)
            p2 = port_s[n2] + 1
            port_s[n2] += 1
            print(n1, n2, p1, p2)
            pair_s.append([n1, n2])
            edge_s.append([n1, p1, n2, p2])'''

        # print(edge_s)

        random_graph = 'self.init_with_dicts(' + str(number_of_node) + ', ['

        num_of_edges = len(edge_s)
        # print(num_of_edges)
        k = 0
        for edge in edge_s:
            if k != num_of_edges - 1:
                random_graph = random_graph + 'dict(n1=' + str(edge[0]) + ', p1=' + str(edge[1]) + ',' \
                                                                                                   ' n2=' + str(
                    edge[2]) + ', p2=' + str(edge[3]) + '),'
            else:
                break
            k += 1

        random_graph = random_graph + 'dict(n1=' + str(edge_s[k][0]) + ', p1=' + str(edge_s[k][1]) + ',' \
                                                                                                     ' n2=' + str(
            edge_s[k][2]) + ', p2=' + str(edge_s[k][3]) + ')])'

        G = exec(random_graph)
        return G
