import networkx as nx
import pygame
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
from pygame.locals import *
import time

class Plot:
    def __init__(self, graph, pos):
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('monospace', 20)
        self.graph = graph
        self.pos = pos
        self.fig = pylab.figure(figsize=[16, 8], dpi=100)
        self.window = pygame.display.set_mode((1600, 800), DOUBLEBUF)
        self.screen = pygame.display.get_surface()

        self.prev_backtrack_node = -1

    # if the user wants to close the window after the algorithm is finished
    def has_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def initialize_colors(self):
        for u, v in self.graph.edges():
            self.graph[u][v]['color'] = 'black'
            self.graph[u][v]['width'] = 0.3
            self.graph.nodes[u]['color'] = 'lightblue'
            self.graph.nodes[v]['color'] = 'lightblue'
            
    def clear_edge_colors(self):
        for u, v in self.graph.edges():
            self.graph[u][v]['color'] = 'black'
            if self.graph[u][v]['width'] == 5:
                self.graph[u][v]['width'] = 3

    def color_forward_edge(self, from_, to):
        self.graph.edges[from_, to]['color'] = 'green'
        self.graph.edges[from_, to]['width'] = 5
        self.graph.nodes[from_]['color'] = 'green'

    def color_reverse_edge(self, from_, to):
        self.graph.edges[from_, to]['color'] = 'orange'
        self.graph.edges[from_, to]['width'] = 5
        self.graph.nodes[from_]['color'] = 'orange'

    def color_backtrack_edge(self, from_, to):
        self.graph.edges[from_, to]['color'] = 'red'
        self.graph.edges[from_, to]['width'] = 5
        self.graph.nodes[from_]['color'] = 'red'
        if self.prev_backtrack_node != -1:
            self.graph.nodes[self.prev_backtrack_node]['color'] = 'lightblue'
        self.prev_backtrack_node = from_

    def draw_window(self, texts):
        edge_colors = [self.graph[u][v]['color'] for u, v in self.graph.edges()]
        edge_widths = [self.graph[u][v]['width'] for u, v in self.graph.edges()]
        node_colors = [self.graph.nodes[n]['color'] for n in self.graph.nodes()]
        self.fig.clf()

        if self.pos == None:
            my_pos = nx.spring_layout(self.graph, seed=100)
        else:
            my_pos = self.pos
        nx.draw_networkx_nodes(self.graph, my_pos)
        nx.draw_networkx_edges(self.graph, my_pos)
        node_labels = nx.get_node_attributes(self.graph, 'id')
        formatted_edge_labels = self.graph.get_edge_labels()

        nx.draw_networkx_edge_labels(self.graph,my_pos,edge_labels=formatted_edge_labels,label_pos=0.3,font_color='red')
        nx.draw_networkx_labels(self.graph, pos=my_pos)
        nx.draw(self.graph, node_color=node_colors, edge_color=edge_colors, pos=my_pos)
        nx.draw_networkx_edges(self.graph, my_pos, edge_color=edge_colors, width=edge_widths)

        plt.tight_layout(rect=(0.1, 0, 1, 0.9))
        canvas = agg.FigureCanvasAgg(self.fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.screen.blit(surf, (0, 0))
        y = 0
        for text in texts:
            textsurface = self.myfont.render(text, False, (0, 0, 0))
            self.screen.blit(textsurface, (0, y))
            y += 22

    def step_by_step_display(self, all_paths_exploration_stats):
        running = True
                    
        attempts = 0
        for path_exploration_stats in all_paths_exploration_stats:
            self.initialize_colors()
            attempts += 1
            idx = 0
            f_tour = path_exploration_stats.f_tour
            exploration_sequence = path_exploration_stats.exploration_sequence
            for from_, to, port_taken, direction in exploration_sequence:
                if self.has_quit():
                    running = False
                    break
                idx += 1

                text = ['Port sequence: ' + ''.join(str(x) for x in f_tour),
                        'Ports taken  : ' + ''.join(str(x) for _, _, x, _ in exploration_sequence[:idx]),
                       'Current route is rooted at node: ' + str(path_exploration_stats.actual_root_id),
                       'Current node: ' + str(from_),
                       'Port chosen: ' + str(port_taken),
                       'Next node: ' + str(to),
                       'Attempts: ' + str(attempts)]

                # color only the currently used edge
                self.clear_edge_colors()
                if direction == "forward":
                    self.color_forward_edge(from_, to)
                elif direction == 'reverse':
                    self.color_reverse_edge(from_, to)
                elif direction == 'backtrack':
                    self.color_backtrack_edge(from_, to)
                    text[1] += ' (backtracking to start...)'
                else:
                    assert False, "Unknown exploration direction: {}!".format(direction)

                self.draw_window(text)
                pygame.display.flip()
                time.sleep(0.3)
        while running:
            if self.has_quit():
                running = False
                break

            self.clear_edge_colors()
            self.draw_window(text)
            pygame.display.flip()

    def quick_display_graph(self):
        self.initialize_colors(self)

        running = True
        while running:
            if self.has_quit():
                running = False
                break
            plot.draw_window([])
            pygame.display.flip()
