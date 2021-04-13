import unittest
import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from Node import Graph, MAP_ORACLE, INSTANCE_ORACLE

class TestSum(unittest.TestCase):

    #def test_presented_graph(self):
    #    G = nx.Graph()

    #    G.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
    #    G.add_edges_from([(1, 2), (1, 3), (1, 4),
    #                      (2, 3), (2, 4),
    #                      (3, 4),
    #                      (4, 5), (4, 6), (4, 7), (4, 8),
    #                      (5, 6), (5, 7), (5, 8),
    #                      (6, 7), (6, 8), (6, 9), (6, 10),
    #                      (7, 11), (7, 12),
    #                      (9, 10),
    #                      (11, 12),
    #                      (12, 13), (12, 14), (12, 15),
    #                      (14, 16), (14, 17),
    #                      (15, 18), (15, 21),
    #                      (16, 17),
    #                      (18, 19), (18, 20),
    #                      (21, 22), (21, 23), (21, 24),
    #                      (22, 23), (22, 24),
    #                      (23, 24)])
    #    nodes = [Node(1, [Port(1, 2), Port(1, 3), Port(1, 4)]),
    #             Node(2, [Port(1, 2), Port(2, 3), Port(2, 4)]),
    #             Node(3, [Port(1, 3), Port(2, 3), Port(3, 4)]),
    #             Node(4, [Port(1, 4), Port(2, 4), Port(3, 4), Port(4, 5), Port(4, 6), Port(4, 7), Port(4, 8)]),
    #             Node(5, [Port(4, 5), Port(5, 6), Port(5, 7), Port(5, 8)]),
    #             Node(6, [Port(4, 6), Port(5, 6), Port(6, 7), Port(6, 8), Port(6, 9), Port(6, 10)]),
    #             Node(7, [Port(4, 7), Port(5, 7), Port(6, 7), Port(7, 8), Port(7, 11), Port(7, 12)]),
    #             Node(8, [Port(4, 8), Port(5, 8), Port(6, 8), Port(7, 8)]),
    #             Node(9, [Port(6, 9), Port(9, 10)]),
    #             Node(10, [Port(6, 10), Port(9, 10)]),
    #             Node(11, [Port(7, 11), Port(11, 12)]),
    #             Node(12, [Port(6, 12), Port(11, 12), Port(12, 13), Port(12, 14), Port(12, 15)]),
    #             Node(13, [Port(12, 13)]),
    #             Node(14, [Port(12, 14), Port(14, 16), Port(14, 17)]),
    #             Node(15, [Port(12, 15), Port(15, 18), Port(15, 21)]),
    #             Node(16, [Port(14, 16), Port(16, 17)]),
    #             Node(17, [Port(14, 17), Port(16, 17)]),
    #             Node(18, [Port(15, 18), Port(18, 19), Port(18, 20)]),
    #             Node(19, [Port(18, 19)]),
    #             Node(20, [Port(18, 20)]),
    #             Node(21, [Port(15, 21), Port(21, 22), Port(21, 23), Port(21, 24)]),
    #             Node(22, [Port(21, 22), Port(22, 23), Port(22, 24)]),
    #             Node(23, [Port(21, 23), Port(22, 23), Port(23, 24)]),
    #             Node(24, [Port(21, 23), Port(22, 24), Port(23, 24)])]

    #    NewGraph = Graph(G, nodes)
    #    robot_pos = 1
    #    NewGraph.encode(MAP_ORACLE, robot_pos)

    #    assert(NewGraph.path == [1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1])
    #    assert(NewGraph.back_source == [0, 0, 0])
    #    assert(NewGraph.node_path == [1, 2, 1, 3, 1, 4, 5, 4, 6, 9, 6, 10, 6, 4, 7, 11, 7, 12, 13, 12, 14, 16, 14, 17, 14, 12, 15, 18, 19, 18, 20, 18, 15, 21, 22, 21, 23, 21, 24, 21, 15, 12, 7, 4, 8])
    #    assert(NewGraph.ports == ['00000', '00000', '00001', '00000', '00010', '00011', '00000', '00100', '00100', '00000', '00101', '00000', '00000', '00101', '00100', '00000', '00101', '00010', '00000', '00011', '00001', '00000', '00010', '00000', '00000', '00100', '00001', '00001', '00000', '00010', '00000', '00000', '00010', '00001', '00000', '00010', '00000', '00011', '00011', '00000', '00000', '00101', '00000', '00110'])

    #---------------------------------------------------------------------------

    #       (1)
    #       0
    #      /
    #     2
    #    (0) 0----------0 (4)
    #     1
    #      \
    #       0
    #        (2) 1----0 (3)
    def test_tiny_graph_from_dict(self):

        NewGraph = Graph()
        Graph.get_random_graph(NewGraph, 10)
        """NewGraph.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])"""

        robot_pos = 0
        # NewGraph.encode(INSTANCE_ORACLE, robot_pos)
        #NewGraph.encode_with_plotting(INSTANCE_ORACLE, robot_pos)
        NewGraph.print_encoding_info()
        my_pos = nx.spring_layout(NewGraph.G, seed=100)
        my_pos = nx.spring_layout(NewGraph.G, seed=100)
        print(NewGraph.encode(INSTANCE_ORACLE, robot_pos))

        # Ideally, we should check structural equivalence.
        # assert self.path == [1, 0, 1, 0, 1, 1, 0, 0]
        # assert self.ports_decimal == [2, 0, 0, 0, 1, 1, 0, 0]

    def test_tiny_graph_from_decode(self):
        GraphToEncode = Graph()
        GraphToEncode.init_with_dicts(5, [
            dict(n1=0, p1=2, n2=1, p2=0),
            dict(n1=0, p1=0, n2=4, p2=0),
            dict(n1=0, p1=1, n2=2, p2=0),
            dict(n1=2, p1=1, n2=3, p2=0)
        ])

        robot_pos = 2
        oracle_type = 'MAP_ORACLE'
        NewGraph = Graph()
        NewGraph.init_with_decode(GraphToEncode.encode(oracle_type, robot_pos))
        # TODO: Check structural equivalence.
        NewGraph.get_edge_labels()

        if oracle_type == 'MAP_ORACLE':
            f_tours = NewGraph.get_map_oracle_f_tours()
           # NewGraph.map_oracle_with_plotting()
            NewGraph.map_oracle_robot(f_tours, robot_pos, None)

        pos = nx.spring_layout(NewGraph.G)
        nx.draw(NewGraph.G, pos, with_labels=True, font_weight='bold')
        formatted_edge_labels = NewGraph.get_edge_labels()
        nx.draw_networkx_edge_labels(NewGraph.G, pos, edge_labels=formatted_edge_labels, label_pos=0.3,
                                     font_color='red')
        plt.show()

        NewGraph.print_graph()
        NewGraph.get_edge_labels()
        
        # TODO: Check structural equivalence.

        # pos = nx.spring_layout(NewGraph.G)
        # nx.draw(NewGraph.G, pos, with_labels=True, font_weight='bold')
        # formatted_edge_labels = NewGraph.get_edge_labels()
        # nx.draw_networkx_edge_labels(NewGraph.G,pos,edge_labels=formatted_edge_labels,label_pos=0.3,font_color='red')
        # plt.show()

if __name__ == '__main__':
    unittest.main()
