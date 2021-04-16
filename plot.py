import networkx as nx
import pygame
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import plot
import pylab
from pygame.locals import *
import time

def initialize_colors(graph):
    for u, v in graph.edges():
        graph[u][v]['color'] = 'grey'
        graph[u][v]['width'] = 0.3
        graph[u][v]['visit_count'] = 0
        graph.nodes[u]['color'] = 'lightblue'
        graph.nodes[v]['color'] = 'lightblue'
        
def clear_edge_colors(graph):
    for u, v in graph.edges():
        if graph[u][v]['visit_count'] == 1:
            graph[u][v]['color'] = 'grey'
        elif graph[u][v]['visit_count'] == 2:
            graph[u][v]['color'] = 'black'
        else:
            graph[u][v]['color'] = 'grey'
        if graph[u][v]['width'] == 5:
            graph[u][v]['width'] = 3

def find_next_edge(port):
    next_edge = [port.n1, port.n2]
    #print("Next edge: ", next_edge[0], ", ", next_edge[1])
    return next_edge

def color_forward_edge(graph, from_, to):
    graph.edges[from_, to]['color'] = 'green'
    graph.edges[from_, to]['width'] = 5
    graph.edges[from_, to]['visit_count'] = graph.edges[from_, to]['visit_count'] + 1
    graph.nodes[from_]['color'] = 'green'
    #print("The color of the edge:")
    #print(graph.edges[from_, to]['color'])

def color_reverse_edge(graph, from_, to):
    graph.edges[from_, to]['color'] = 'orange'
    graph.edges[from_, to]['width'] = 5
    graph.nodes[from_]['color'] = 'orange'
    #print("The color of the edge:")
    #print(graph.edges[from_, to]['color'])

def draw_window(graph, game_screen, fig, Graph, pos):
    edge_colors = [graph[u][v]['color'] for u, v in graph.edges()]
    edge_widths = [graph[u][v]['width'] for u, v in graph.edges()]
    node_colors = [graph.nodes[n]['color'] for n in graph.nodes()]
    fig.clf()

    if pos == None:
        my_pos = nx.spring_layout(graph, seed=100)
    else:
        my_pos = pos
    nx.draw_networkx_nodes(graph, my_pos)
    nx.draw_networkx_edges(graph, my_pos)
    node_labels = nx.get_node_attributes(graph, 'id')
    formatted_edge_labels = Graph.G.get_edge_labels()

    nx.draw_networkx_edge_labels(graph,my_pos,edge_labels=formatted_edge_labels,label_pos=0.3,font_color='red')
    nx.draw_networkx_labels(graph, pos=my_pos)
    nx.draw(graph, node_color=node_colors, edge_color=edge_colors, pos=my_pos)
    nx.draw_networkx_edges(graph, my_pos, edge_color=edge_colors, width=edge_widths)
    plt.tight_layout()
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    game_screen.blit(surf, (0, 0))

def init_environment():
    pygame.init()
    fig = pylab.figure(figsize=[7, 5], dpi=100)
    window = pygame.display.set_mode((1600, 800), DOUBLEBUF)
    screen = pygame.display.get_surface()
