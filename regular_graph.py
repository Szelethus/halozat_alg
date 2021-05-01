from PortNumberedGraph import PortNumberedGraph

def get_regular_graph():
    Graph = PortNumberedGraph()
    Graph.init_with_dicts(5, [

        dict(n1=0, p1=0, n2=1, p2=3),
        dict(n1=0, p1=1, n2=2, p2=2),
        dict(n1=0, p1=2, n2=3, p2=1),
        dict(n1=0, p1=3, n2=4, p2=0),

        dict(n1=1, p1=0, n2=2, p2=3),
        dict(n1=1, p1=1, n2=3, p2=2),
        dict(n1=1, p1=2, n2=4, p2=1),

        dict(n1=2, p1=0, n2=3, p2=3),
        dict(n1=2, p1=1, n2=4, p2=2),

        dict(n1=3, p1=0, n2=4, p2=3),

    ])

    pos = {
        0  : (100, 100),
        1  : ( 80, 200),
        2  : (150, 250),
        3  : (200, 100),
        4  : (220, 200)
    }
    return Graph, pos