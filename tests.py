import unittest
import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from PortNumberedGraph import PortNumberedGraph
from Oracle import Oracle, MAP_ORACLE, INSTANCE_ORACLE
from Robot import Robot
from Plot import Plot
from GraphGenerator import GraphGenerator
import evaluate_metrics as ev
import csv_helper

def edge_attr_equivalence(attr1, attr2):
    print('_-------')
    print(attr1)
    print(attr2)
    return True

class TestSum(unittest.TestCase):

    #       (1)
    #       0
    #      /
    #     2
    #    (0) 0----------0 (4)
    #     1
    #      \
    #       0
    #        (2) 1----0 (3)    
    def test_encode_instance_default_start_node(self):
        filename = csv_helper.create_unique_filename("test")
        csv_helper.opencsv(filename)
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 0
        instance_oracle = Oracle(INSTANCE_ORACLE, GraphToEncode)

        encoded_route, path, node_path, ports, ports_decimal, spanning_tree = instance_oracle.encode_with_stats(robot_pos)

        csv_helper.write_new_datas(filename, [ev.get_number_of_edges(GraphToEncode), ev.get_number_of_nodes(GraphToEncode), ev.get_graph_density(GraphToEncode), ev.get_number_of_leaves(spanning_tree) ])

        assert encoded_route == '1101011000010000000000001001000000'
        assert path == [1, 0, 1, 0, 1, 1, 0, 0]
        assert node_path == [1, 0, 4, 0, 2, 3, 2, 0]
        assert ports == ['010', '000', '000', '000', '001', '001', '000', '000']

    def test_encode_instance_3_start_node(self):
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 3
        instance_oracle = Oracle(INSTANCE_ORACLE, GraphToEncode)

        encoded_route, path, node_path, ports, ports_decimal, _ = instance_oracle.encode_with_stats(robot_pos)

        assert encoded_route == '1111010000000000010000000000001001'
        assert path == [1, 1, 1, 0, 1, 0, 0, 0]
        assert node_path == [2, 0, 1, 0, 4, 0, 2, 3]
        assert ports == ['000', '000', '010', '000', '000', '000', '001', '001']

    def test_encode_map_3_start_node(self):
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 3
        map_oracle = Oracle(MAP_ORACLE, GraphToEncode)

        encoded_route, path, node_path, ports, ports_decimal, _ = map_oracle.encode_with_stats(robot_pos)

        assert encoded_route == '0101011000010000000000001001000000'
        assert path == [1, 0, 1, 0, 1, 1, 0, 0]
        assert node_path == [1, 0, 4, 0, 2, 3, 2, 0]
        assert ports == ['010', '000', '000', '000', '001', '001', '000', '000']


    def test_tiny_graph_from_decode(self):
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 0
        map_oracle = Oracle(MAP_ORACLE, GraphToEncode)

        encoded_route, _, _, _, _, spanning_tree = map_oracle.encode_with_stats(robot_pos)
        robot = Robot(encoded_route)

        assert nx.is_isomorphic(spanning_tree, robot.G) #, edge_match=edge_attr_equivalence)

    def test_map_oracle(self):
        NewGraph = PortNumberedGraph()
        NewGraph.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 2
        map_oracle = Oracle(MAP_ORACLE, NewGraph)

        robot = Robot(map_oracle.encode(robot_pos))

        print(robot.traverse(NewGraph, robot_pos))


    def test_random_graph(self):
        graph_generator = GraphGenerator()
        NewGraph = graph_generator.get_random_graph(10)

        robot_pos = 0
        # NewGraph.encode(INSTANCE_ORACLE, robot_pos)
        #NewGraph.encode_with_plotting(INSTANCE_ORACLE, robot_pos)
        my_pos = nx.spring_layout(NewGraph, seed=100)
        my_pos = nx.spring_layout(NewGraph, seed=100)
        #NewGraph.print_encoding_info(INSTANCE_ORACLE, robot_pos)

if __name__ == '__main__':
    unittest.main()
