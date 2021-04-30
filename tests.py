import unittest
import math

import networkx as nx

from PortNumberedGraph import PortNumberedGraph
from Oracle import MapOracle, InstanceOracle
from Robot import Robot
from Plot import Plot
from GraphGenerator import GraphGenerator
import csv_helper
from Statistics import CombinedStatistics, get_combined_csv_columns

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
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 0
        instance_oracle = InstanceOracle(GraphToEncode, robot_pos)

        stats = instance_oracle.encode_with_stats()

        assert stats.code == '1101011000010000000000001001000000'
        assert stats.path == [1, 0, 1, 0, 1, 1, 0, 0]
        assert stats.node_path == [1, 0, 4, 0, 2, 3, 2, 0]
        assert stats.ports == ['010', '000', '000', '000', '001', '001', '000', '000']

    def test_encode_instance_3_start_node(self):
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 3
        instance_oracle = InstanceOracle(GraphToEncode, robot_pos)

        stats = instance_oracle.encode_with_stats()

        assert stats.code == '1111010000000000010000000000001001'
        assert stats.path == [1, 1, 1, 0, 1, 0, 0, 0]
        assert stats.node_path == [2, 0, 1, 0, 4, 0, 2, 3]
        assert stats.ports == ['000', '000', '010', '000', '000', '000', '001', '001']

    def test_encode_map_3_start_node(self):
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 3
        map_oracle = MapOracle(GraphToEncode)

        stats = map_oracle.encode_with_stats()

        assert stats.code == '0101011000010000000000001001000000'
        assert stats.path == [1, 0, 1, 0, 1, 1, 0, 0]
        assert stats.node_path == [1, 0, 4, 0, 2, 3, 2, 0]
        assert stats.ports == ['010', '000', '000', '000', '001', '001', '000', '000']


    def test_tiny_graph_from_decode(self):
        GraphToEncode = PortNumberedGraph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 0
        map_oracle = MapOracle(GraphToEncode)

        stats = map_oracle.encode_with_stats()
        robot = Robot(stats.code)

        assert nx.is_isomorphic(stats.spanning_tree, robot.G) #, edge_match=edge_attr_equivalence)

    def test_map_oracle(self):
        NewGraph = PortNumberedGraph()
        NewGraph.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 2
        map_oracle = MapOracle(NewGraph)

        robot = Robot(map_oracle.encode())

        print(robot.traverse(NewGraph, robot_pos))

    def test_map_oracle_csv(self):
        new_graph = PortNumberedGraph()
        new_graph.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        map_oracle = MapOracle(new_graph)
        oracle_stats = map_oracle.encode_with_stats()
        robot = Robot(oracle_stats.code)

        filename = "map_oracle_test"
        csv_helper.opencsv(filename, get_combined_csv_columns())

        for robot_pos in new_graph.nodes():
            explorations_stats = robot.traverse(new_graph, robot_pos)
            combined_stats = CombinedStatistics(new_graph, oracle_stats, explorations_stats)
            combined_stats.fill_csv(filename)

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
