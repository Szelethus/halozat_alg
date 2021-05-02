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

    robot_positions = [x * math.floor(len(graph.nodes()) / 10) for x in range(10)]

    for idx, robot_pos in enumerate(robot_positions):
        print('Robot starting at positions', idx + 1, '/', len(robot_positions)) 
        explorations_stats = robot.traverse(graph, robot_pos)
        combined_stats = CombinedStatistics(graph, oracle_stats, explorations_stats)
        combined_stats.fill_csv(filename)

