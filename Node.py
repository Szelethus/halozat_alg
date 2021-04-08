import networkx as nx
from networkx import minimum_spanning_tree
import math

MAP_ORACLE = 0
INSTANCE_ORACLE = 1

def get_bin(x, n=0):
    return format(x, 'b').zfill(n)

class Graph:
    def __init__(self, nx_graph, node_index):
        self.nx_graph = nx_graph
        self.node_index = node_index
        self.path = []
        self.node_path = []
        self.back_source = []
        self.ports = []

    def encode(self, oracle_type, robot_pos):
        if oracle_type == INSTANCE_ORACLE:
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.nx_graph), robot_pos)
        else:
            #edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.nx_graph), random.randint(1, self.nx_graph.number_of_nodes()))
            # Lets not make it random, otherwise it wouldn't be deterministic
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.nx_graph), 1)

        visited_nodes = 0
        bit = math.ceil(math.log(self.nx_graph.number_of_nodes(), 2))
        for u, v, d in edges:
            found = False
            if visited_nodes != self.nx_graph.number_of_nodes():
                if d == "forward":
                    self.path.append(1)
                    self.node_path.append(v)
                    visited_nodes += 1
                    for nod in self.node_index:
                        k = 0
                        for por in nod.ports:
                            if u == por.to_node and v == por.on_port:
                                self.ports.append(get_bin(k, bit))
                                found = True
                            k += 1
                        if found:
                            break
                elif d == 'reverse':
                    self.path.append(0)
                    self.node_path.append(u)
                    for nod in reversed(self.node_index):
                        k = 0
                        for por in nod.ports:
                            if u == por.to_node and v == por.on_port:
                                self.ports.append(get_bin(k, bit))
                                found = True
                            k += 1
                        if found:
                            break
            elif d == 'reverse':
                self.back_source.append(0)

        # The first 1 seems to be excessive, idk why.
        self.path.pop(0)

        return ''.join(str(x) for x in self.path + self.back_source + self.ports)

    def to_string(self):
        print('Structure of the graph (1:forward, 0:reverse): ', self.path)
        print('Back to the source: ', self.back_source)
        print('DFS sequence of nodes: ', self.node_path)
        print('DFS sequence of ports: ', self.ports)

class Node:
    def __init__(self, n_id, ports):
        self.id = n_id
        self.ports = ports

    def allPortTaken(self):
        return all([p.taken for p in self.ports])

    def deg(self):
        return len(self.ports)

    def to_string(self):
        print("id:", self.id, "ports:", self.ports)

class Port:
    def __init__(self, to_node, on_port):
        self.to_node = to_node
        self.on_port = on_port
        self.taken = False

    def to_string(self):
        print("n1:", self.to_node, "n2:", self.on_port, "taken: ", self.taken)

    def equals(self, other):
        return other is not None and self.to_node == other.to_node and self.on_port == other.on_port
