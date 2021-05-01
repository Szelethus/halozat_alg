from PortNumberedGraph import PortNumberedGraph
from Oracle import MapOracle, InstanceOracle
from Robot import Robot
from Plot import Plot
from regular_graph import get_regular_graph
import csv_helper
from Statistics import get_combined_csv_columns
from statistics_gathering import collect_comprehensive_map_statistics

Graph, pos = get_regular_graph()
robot_pos = 1

map_oracle = MapOracle(Graph)
map_oracle.print_encoding_info()
encode_stats = map_oracle.encode_with_stats()
robot = Robot(encode_stats.code)
exploration_stats = robot.traverse(Graph, robot_pos)
for stat in exploration_stats:
    stat.realize_actual_root_ids(encode_stats)

plot = Plot(Graph, pos)
plot.step_by_step_display(exploration_stats)

filename = "regular_graph_stats"
csv_helper.opencsv(filename, get_combined_csv_columns())
collect_comprehensive_map_statistics(filename, Graph)
