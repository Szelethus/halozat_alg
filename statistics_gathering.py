import math
from PortNumberedGraph import PortNumberedGraph
from Oracle import MapOracle
from Robot import Robot
from GraphGenerator import GraphGenerator
import csv_helper
from Statistics import CombinedStatistics

def collect_comprehensive_map_statistics(filename, graph):
    map_oracle = MapOracle(graph)
    map_oracle.root_id = 0
    oracle_stats = map_oracle.encode_with_stats()
    robot = Robot(oracle_stats.code)


    robot_pos = 0
    explorations_stats = robot.traverse(graph, robot_pos)
    combined_stats = CombinedStatistics(graph, oracle_stats, explorations_stats)
    combined_stats.fill_csv(filename)

