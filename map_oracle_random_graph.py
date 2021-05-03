import os
import random

from PortNumberedGraph import PortNumberedGraph
from Oracle import MapOracle, InstanceOracle
from Robot import Robot
from Plot import Plot
from GraphGenerator import GraphGenerator
import csv_helper
from Statistics import get_combined_csv_columns
from statistics_gathering import collect_comprehensive_map_statistics


#Random graph statistics collection with quantity dependent numbers
def get_random_graph_statistics(num_of_nodes, quantity):
    num_of_edges = num_of_nodes - 1
    max_edges = (num_of_nodes * (num_of_nodes - 1)) / 2
    step_size = int(max_edges/quantity)
    seed = 100
    for i in range(quantity):
        graph_generator = GraphGenerator()
        Graph = graph_generator.get_random_graph(num_of_nodes, int(num_of_edges), seed=seed)

        robot_pos = random.randint(0, num_of_nodes)

        map_oracle = MapOracle(Graph)
        map_oracle.print_encoding_info()
        encode_stats = map_oracle.encode_with_stats()
        robot = Robot(encode_stats.code)
        exploration_stats = robot.traverse(Graph, robot_pos)
        for stat in exploration_stats:
            stat.realize_actual_root_ids(encode_stats)

        filename = str(num_of_nodes) + "_" + str(num_of_edges) + "_" + str(seed) + "graph"
        csv_helper.opencsv(filename, get_combined_csv_columns())
        collect_comprehensive_map_statistics(filename, Graph)

        num_of_edges += step_size


#Complete graph statistic
def get_complete_graph_statistic(num_of_nodes):
    seed = 100
    num_of_edges = int((num_of_nodes * (num_of_nodes - 1)) / 2)
    graph_generator = GraphGenerator()
    Graph = graph_generator.get_random_graph(num_of_nodes, num_of_edges, seed=seed)

    robot_pos = robot_pos = random.randint(0, num_of_nodes)

    map_oracle = MapOracle(Graph)
    map_oracle.print_encoding_info()
    encode_stats = map_oracle.encode_with_stats()
    robot = Robot(encode_stats.code)
    exploration_stats = robot.traverse(Graph, robot_pos)
    for stat in exploration_stats:
        stat.realize_actual_root_ids(encode_stats)

    filename = str(num_of_nodes) + "_" + str(num_of_edges) + "_" + str(seed) + "graph"
    csv_helper.opencsv(filename, get_combined_csv_columns())
    collect_comprehensive_map_statistics(filename, Graph)


get_random_graph_statistics(200, 150)
get_random_graph_statistics(300, 100)
get_random_graph_statistics(400, 210)

