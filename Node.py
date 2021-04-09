import networkx as nx
from networkx import minimum_spanning_tree
import math

MAP_ORACLE = 0
INSTANCE_ORACLE = 1

def get_binary(x, n=0):
    return format(x, 'b').zfill(n)

class Graph:
    def __init__(self, node_count, edges_with_ports):
        self.path = []
        self.node_path = []
        self.ports = []
        self.ports_decimal = []

        self.G = nx.Graph()

        # https://stackoverflow.com/questions/57095809/networkx-connecting-nodes-using-ports
    
        # Initialize the graph with the nodes with only a single port.
        # (the graph must be connected, so this this is okay, tho verification would
        # be nice)
        for i in range(0, node_count):
            self.G.add_node(i, ports=[0])
    
        # Count how many ports each of the nodes have by inspecting the edge list.
        idx = 0
        while idx < len(edges_with_ports):
            current_edge_count = 0
            current_node = edges_with_ports[idx]['n1']
            while idx < len(edges_with_ports) and edges_with_ports[idx]['n1'] == current_node:
                current_edge_count = current_edge_count + 1
                idx = idx + 1
                self.G.nodes(data=True)[current_node]['ports'].append(current_edge_count)
    
        # Connect these ports with edges.
        for e in edges_with_ports:
            self.add_edge_port(e['n1'], e['p1'], e['n2'], e['p2'])
    
    def verify_nodes_and_ports(self, node, port):
        if self.G.nodes().get(node, None) is None:
            print("Node : {} is not present in Graph".format(node))
            return False
    
        if self.G.nodes(data=True)[node]['ports'][port] is None:
            print("Port ID :{} is incorrect for Node ID : {}!".
                  format(node, port))
        return False
    
        return True
    
    
    def add_edge_port(self, node1, port1, node2, port2):
        self.verify_nodes_and_ports(node1, port1)
        self.verify_nodes_and_ports(node2, port2)
    
        self.G.add_edge(node1, node2, n1=node1, p1=port1, n2=node2, p2=port2)

    def get_port_to(self, from_, to):
        data = self.G.get_edge_data(from_, to)
        if (data['n1'] == from_):
            return data['p1']
        else:
            return data['p2']

    def encode(self, oracle_type, robot_pos):
        if oracle_type == INSTANCE_ORACLE:
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), robot_pos)
        else:
            # Lets not make it random, otherwise it wouldn't be deterministic
            edges = nx.dfs_labeled_edges(minimum_spanning_tree(self.G), 1)

        visited_nodes = 0
        bit = math.ceil(math.log(self.G.number_of_nodes(), 2))
        for u, v, d in edges:
            if u == v:
                continue
            if visited_nodes != self.G.number_of_nodes():
                if d == "forward":
                    self.path.append(1)
                    self.node_path.append(u)
                    visited_nodes += 1
                    self.ports.append(get_binary(self.get_port_to(u, v), bit))
                    self.ports_decimal.append(self.get_port_to(u, v))
                elif d == 'reverse':
                    self.path.append(0)
                    self.node_path.append(v)
                    self.ports.append(get_binary(self.get_port_to(v, u), bit))
                    self.ports_decimal.append(self.get_port_to(v, u))
            #elif d == 'reverse':
            #    self.back_source.append(0)

        return ''.join(str(x) for x in self.path + [0] + self.ports)

    def decode(self, code):
        G = nx.Graph()

        # Add a root.
        G.add_node(0, ports=[])
        current_node = 0
        # Parent stack. Last element is the parent of the current node, the one
        # before that is the parent of the last element, and so on.
        parents = []
        
        for c in code:
            # We finished parsing the structure of the graph.
            if current_node == 0 and c == '0':
                break;
            # 0 means "go up in the tree".
            elif c == '0':
                current_node = parents.pop()
            # 1 means "go down in the tree" (to an unvisited node).
            else:
                new_node = G.number_of_nodes()
                G.add_node(new_node, ports=[0])
                G.add_edge(current_node, new_node);
                G.nodes(data=True)[current_node]['ports'].append(len(G.edges(current_node)) - 1)
                parents.append(current_node)
                current_node = new_node
        return G


    def to_string(self):
        print('Structure of the graph (1:forward, 0:reverse): ', self.path)
        print('DFS sequence of nodes: ', self.node_path)
        print('DFS sequence of ports: ', self.ports)
        print('DFS sequence of ports in decimal: ', self.ports_decimal)
