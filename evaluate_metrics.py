import networkx as nx


def get_number_of_leaves(graph):
    return sum([1 for node in graph if graph.degree(node)==1])

def get_number_of_different_edges(spanning_tree, edges):
    nontree = 0
    reverse = 0
    forward = 0
    for u,v, d in edges:
        if d == "forward":
            forward = forward + 1
        elif d == "reverse":
            reverse = reverse + 1
        elif d == "nontree":
            nontree = nontree + 1
    return forward, reverse, nontree

def get_number_of_edges(graph):
    return len(graph.edges)

def get_number_of_nodes(graph):
    return len(graph.nodes)

def get_graph_density(graph):
    if(get_number_of_nodes(graph) > 0):
        return get_number_of_edges(graph)/get_number_of_nodes(graph)
    return 0

