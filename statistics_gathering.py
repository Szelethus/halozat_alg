import unittest
import math
import random

import networkx as nx
from networkx import minimum_spanning_tree
import matplotlib.pyplot as plt

from PortNumberedGraph import PortNumberedGraph
from Oracle import MapOracle, InstanceOracle
from Robot import Robot
from Plot import Plot
from GraphGenerator import GraphGenerator
import csv_helper
from Statistics import CombinedStatistics

def collect_comprehensive_map_statistics(filename, graph):
    for root in graph.nodes():
        map_oracle = MapOracle(graph)
        map_oracle.root_id = root
        oracle_stats = map_oracle.encode_with_stats()
        robot = Robot(oracle_stats.code)

        for robot_pos in graph.nodes():
            explorations_stats = robot.traverse(graph, robot_pos)
            combined_stats = CombinedStatistics(graph, oracle_stats, explorations_stats)
            #print('writing statistics for root', root, 'and starting pos', robot_pos)
            combined_stats.fill_csv(filename)

