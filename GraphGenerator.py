import math
import os

import pygame
import pylab
from pygame.locals import *
import time
import random
from PortNumberedGraph import PortNumberedGraph

class GraphGenerator:
    def get_random_graph(self, number_of_nodes, number_of_edges=None, seed=None):
        node_s = []
        port_s = list()
        edge_s = []
        pair_s = []
        if seed is None:
            seed = random.randint(0, 100)
        random.seed(seed)
        num_of_max_edge_number = number_of_nodes*((number_of_nodes-1)/2)
        if number_of_edges is None:
            number_of_edges = random.randint(0, num_of_max_edge_number)
        if((number_of_edges < number_of_nodes - 1 or number_of_edges > num_of_max_edge_number)
                and number_of_edges is not None):
           return print('Error: the number of edges or nodes is incorrect!')
        else:
            # add first n1, p1, n2, p2
            for i in range(number_of_nodes):
                port_s.insert(i, 0)
            n1 = random.randint(0, number_of_nodes - 1)
            p1 = 0
            node_s.append(n1)
            n2 = random.randint(0, number_of_nodes - 1)
            while (n2 == n1):
                n2 = random.randint(0, number_of_nodes - 1)
            p2 = 0
            node_s.append(n2)
            print(n1, n2, p1, p2)
            pair_s.append([n1, n2])
            edge_s.append([n1, p1, n2, p2])
            # add other n1, p1, n2, p2 in a spanning tree
            for i in range(1, number_of_nodes - 1):
                n1 = random.choice(node_s)
                p1 = port_s[n1] + 1
                port_s[n1] += 1
                n2 = random.randint(0, number_of_nodes - 1)
                while n2 in node_s:
                    n2 = random.randint(0, number_of_nodes - 1)
                p2 = 0
                node_s.append(n2)
                print(n1, n2, p1, p2)
                pair_s.append([n1, n2])
                edge_s.append([n1, p1, n2, p2])

            # add extra edges to the tree if you don't just need tree
            for i in range(0, number_of_edges - (number_of_nodes-1)):
                n1 = random.randint(0, number_of_nodes - 1)
                n2 = random.randint(0, number_of_nodes - 1)
                while [n1, n2] in pair_s or port_s[n1] == number_of_nodes - 2:
                    n1 = random.randint(0, number_of_nodes - 1)
                p1 = port_s[n1] + 1
                port_s[n1] += 1
                while [n1, n2] in pair_s or [n2, n1] in pair_s or port_s[n2] == number_of_nodes - 2 or n2 == n1:
                    n2 = random.randint(0, number_of_nodes - 1)
                p2 = port_s[n2] + 1
                port_s[n2] += 1
                print(n1, n2, p1, p2)
                pair_s.append([n1, n2])
                edge_s.append([n1, p1, n2, p2])

            # print(edge_s)
            G = PortNumberedGraph()
            random_graph = 'G.init_with_dicts(' + str(number_of_nodes) + ', ['

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

            exec(random_graph)
            #random_graph_to_txt = random_graph + '\r\n'
            if not os.path.exists('Graphs'):
                os.makedirs('Graphs')
            f = open("Graphs/graph_"+str(number_of_nodes)+"_"+str(number_of_edges)+"_"+str(seed)+".txt", "w")
            f.write(random_graph)
            f.close()
            return G
