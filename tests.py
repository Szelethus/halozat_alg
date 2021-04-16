import unittest
import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from Node import Graph, MAP_ORACLE, INSTANCE_ORACLE

def edge_attr_equivalence(attr1, attr2):
    print('_-------')
    print(attr1)
    print(attr2)
    return True

class TestSum(unittest.TestCase):

#    #       (1)
#    #       0
#    #      /
#    #     2
#    #    (0) 0----------0 (4)
#    #     1
#    #      \
#    #       0
#    #        (2) 1----0 (3)
#    def test_random_graph(self):
#
#        NewGraph = Graph()
#        Graph.get_random_graph(NewGraph, 10)
#        """NewGraph.init_with_dicts(5, [
#            dict(n1=0, p1=2, n2=1, p2=0),
#            dict(n1=0, p1=0, n2=4, p2=0),
#            dict(n1=0, p1=1, n2=2, p2=0),
#            dict(n1=2, p1=1, n2=3, p2=0)
#        ])"""
#
#        robot_pos = 0
#        # NewGraph.encode(INSTANCE_ORACLE, robot_pos)
#        #NewGraph.encode_with_plotting(INSTANCE_ORACLE, robot_pos)
#        my_pos = nx.spring_layout(NewGraph.G, seed=100)
#        my_pos = nx.spring_layout(NewGraph.G, seed=100)
#        #NewGraph.print_encoding_info(INSTANCE_ORACLE, robot_pos)
#
#        # Ideally, we should check structural equivalence.
#        # assert self.path == [1, 0, 1, 0, 1, 1, 0, 0]
#        # assert self.ports_decimal == [2, 0, 0, 0, 1, 1, 0, 0]

    def test_tiny_graph_from_decode(self):
        GraphToEncode = Graph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 0
        oracle_type = 'MAP_ORACLE'

        encoded_route, _, _, _, _, spanning_tree = GraphToEncode.encode(oracle_type, robot_pos)
        GraphToEncode.print_encoding_info(INSTANCE_ORACLE, robot_pos)

        NewGraph = Graph()
        NewGraph.init_with_decode(encoded_route)
        #nx.draw(GraphToEncode.G, with_labels=True, font_weight='bold')
        #plt.show()
        #nx.draw(GraphToEncode.G, with_labels=True, font_weight='bold')
        #plt.show()
        #nx.draw(spanning_tree, with_labels=True, font_weight='bold')
        #plt.show()
        assert nx.is_isomorphic(GraphToEncode.G, NewGraph.G, edge_match=edge_attr_equivalence)
        # TODO: Check structural equivalence.
        

#    def test_map_oracle(self):
#        GraphToEncode = Graph()
#        GraphToEncode.init_with_dicts(5, [
#            dict(n1=0, p1=2, n2=1, p2=0),
#            dict(n1=0, p1=0, n2=4, p2=0),
#            dict(n1=0, p1=1, n2=2, p2=0),
#            dict(n1=2, p1=1, n2=3, p2=0)
#        ])
#
#        robot_pos = 2
#        oracle_type = 'MAP_ORACLE'
#
#        NewGraph = Graph()
#        NewGraph.init_with_decode(GraphToEncode.encode(oracle_type, robot_pos))
#        # TODO: Check structural equivalence.
#
#        if oracle_type == 'MAP_ORACLE':
#            f_tours = NewGraph.get_map_oracle_f_tours()
#           # NewGraph.map_oracle_with_plotting()
#            NewGraph.map_oracle_robot(f_tours, robot_pos, None)
#
#        pos = nx.spring_layout(NewGraph.G)
#        nx.draw(NewGraph.G, pos, with_labels=True, font_weight='bold')
#        formatted_edge_labels = NewGraph.get_edge_labels()
#        nx.draw_networkx_edge_labels(NewGraph.G, pos, edge_labels=formatted_edge_labels, label_pos=0.3,
#                                     font_color='red')
#        plt.show()
#
#        NewGraph.print_graph()
#        NewGraph.get_edge_labels()
#        
#        # TODO: Check structural equivalence.
#
#        # pos = nx.spring_layout(NewGraph.G)
#        # nx.draw(NewGraph.G, pos, with_labels=True, font_weight='bold')
#        # formatted_edge_labels = NewGraph.get_edge_labels()
#        # nx.draw_networkx_edge_labels(NewGraph.G,pos,edge_labels=formatted_edge_labels,label_pos=0.3,font_color='red')
#        # plt.show()

if __name__ == '__main__':
    unittest.main()
