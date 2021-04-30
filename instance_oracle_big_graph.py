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
from big_graph import get_big_graph

Graph, pos = get_big_graph()
robot_pos = 0

instance_oracle = InstanceOracle(Graph, robot_pos)
instance_oracle.print_encoding_info()

# CANT BE BOTHERED TO FIX THIS CRAP
robot = Robot(instance_oracle.encode())
plot = Plot(Graph, pos)
plot.step_by_step_display(robot.traverse(Graph, robot_pos))
