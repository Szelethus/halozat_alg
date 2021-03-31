import networkx as nx
import matplotlib.pyplot as plt

def encode(structure, port_numbering):
    return structure + \
           ('0' * nx.shortest_path_length(decode(structure), 0, decode(structure).number_of_nodes() - 1)) + \
           port_numbering


def decode(code):
    G = nx.Graph()

    # Add a root.
    G.add_node(0)
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
            G.add_node(new_node)
            G.add_edge(current_node, new_node);
            parents.append(current_node)
            current_node = new_node
    return G


#https://stackoverflow.com/questions/57095809/networkx-connecting-nodes-using-ports

#Ghetto way of constructing a code:
print(encode ("1101111010110100010100111111010110100010100111111011", "r"))
G = decode("110011111000011101101110001110100110101");
print(G.nodes)
print(nx.shortest_path_length(G, 0, G.number_of_nodes() - 1))
print(G.edges)
print(nx.to_nested_tuple(G, 0))
nx.draw(G, with_labels=True, font_weight='bold')
plt.show()
