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


class GraphGenerator:
    
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
