import networkx as nx
import pygame
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg

def clear_edge_colors(graph):
    for u, v in graph.edges():
        graph[u][v]['color'] = 'black'

def find_next_edge(port):
    next_edge = [port.n1, port.n2]
    print("Next edge: ", next_edge[0], ", ", next_edge[1])
    return next_edge

def color_forward_edge(graph, next_edge):
    i = next_edge[0]
    j = next_edge[1]
    graph.edges[i, j]['color'] = 'red'

def color_reverse_edge(graph, next_edge):
    i = next_edge[0]
    j = next_edge[1]
    graph.edges[i, j]['color'] = 'orange'

def draw_window(graph, game_screen, fig):
    edges = graph.edges()
    colors = [graph[u][v]['color'] for u, v in edges]
    fig.clf()
    my_pos = nx.spring_layout(graph, seed=100)
    nx.draw_networkx_nodes(graph, my_pos)
    nx.draw_networkx_edges(graph, my_pos)
    node_labels = nx.get_node_attributes(graph, 'id')
    nx.draw_networkx_labels(graph, pos=my_pos)
    nx.draw(graph, edge_color=colors, pos=my_pos)
    plt.tight_layout()
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    game_screen.blit(surf, (0, 0))
