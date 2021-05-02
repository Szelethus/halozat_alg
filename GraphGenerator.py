import math
import os
from collections import defaultdict

import pygame
import pylab
from pygame.locals import *
import time
import json
import random
from PortNumberedGraph import PortNumberedGraph


class GraphGenerator:
    def get_random_graph(self, number_of_nodes, number_of_edge=None, seed=None):
        node_s = []
        port_s = list()
        edge_s = []
        pair_s = []
        if seed is None:
            seed = random.randint(0, 100)
        random.seed(seed)
        num_of_max_edge_number = number_of_nodes * ((number_of_nodes - 1) / 2)
        if number_of_edge is None:
            number_of_edges = random.randint(number_of_nodes - 1, num_of_max_edge_number)
        else:
            number_of_edges = number_of_edge
        if number_of_edges < number_of_nodes - 1 or number_of_edges > num_of_max_edge_number:
            assert print('Error: the number of edges or nodes is incorrect!')
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
            for i in range(0, number_of_edges - (number_of_nodes - 1)):
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

            if not os.path.exists('graphs.json'):
                f = open("graphs.json", "w")
                f.write("{\"graphs\":[]}")
                f.close()

            with open('graphs.json') as json_file:
                data = json.load(json_file)

                temp = data['graphs']

                # python object to be appended
                y = {"num_of_nodes": number_of_nodes,
                     "num_of_edges": number_of_edges,
                     "seed": seed,
                     "graph_dict": random_graph
                     }

                # appending data to emp_details
                temp.append(y)

            with open("graphs.json", 'w') as f:
                json.dump(data, f, indent=4)

            return G

    def get_regular_graph(self, number_of_nodes, degree, seed=None):
        node_s = []
        port_s = list()
        edge_s = []
        pair_s = []
        number_of_edges = int(number_of_nodes * degree / 2)
        if seed is None:
            seed = random.randint(0, 100)
        random.seed(seed)
        num_of_max_edge_number = number_of_nodes * ((number_of_nodes - 1) / 2)
        if number_of_edges < number_of_nodes - 1 or number_of_edges > num_of_max_edge_number:
            assert print('Error: the number of edges or nodes is incorrect!')
        elif (number_of_nodes * degree) % 2 != 0:
            assert print("Error: n * d must be even")
        else:
            degrees = []
            for i in range(number_of_nodes):
                degrees.append(0)
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
            degrees[n1] = 1
            degrees[n2] = 1
            # add other n1, p1, n2, p2 in a spanning tree
            for i in range(1, number_of_nodes - 1):
                n1 = random.choice(node_s)
                while degrees[n1]+1 > degree:
                    n1 = random.choice(node_s)
                p1 = port_s[n1] + 1
                port_s[n1] += 1
                n2 = random.randint(0, number_of_nodes - 1)
                while degrees[n2]+1 > degree:
                    n2 = random.randint(0, number_of_nodes - 1)
                degrees[n1] += 1
                degrees[n2] += 1
                while n2 in node_s:
                    n2 = random.randint(0, number_of_nodes - 1)
                p2 = 0
                node_s.append(n2)
                print(n1, n2, p1, p2)
                pair_s.append([n1, n2])
                edge_s.append([n1, p1, n2, p2])

            # add extra edges to the tree if you don't just need tree
            for i in range(0, number_of_edges - (number_of_nodes - 1)):
                n1 = random.randint(0, number_of_nodes - 1)
                while degrees[n1]+1 > degree:
                    n1 = random.randint(0, number_of_nodes - 1)

                n2 = random.randint(0, number_of_nodes - 1)
                while degrees[n2]+1 > degree:
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

            print(random_graph)
            exec(random_graph)

            if not os.path.exists('graphs.json'):
                f = open("graphs.json", "w")
                f.write("{\"graphs\":[]}")
                f.close()

            with open('graphs.json') as json_file:
                data = json.load(json_file)

                temp = data['graphs']

                # python object to be appended
                y = {"num_of_nodes": number_of_nodes,
                     "num_of_edges": number_of_edges,
                     "seed": seed,
                     "graph_dict": random_graph
                     }

                # appending data to emp_details
                temp.append(y)

            with open("graphs.json", 'w') as f:
                json.dump(data, f, indent=4)

            return G


