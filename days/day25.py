import networkx as nx
import matplotlib.pyplot as plt
import math


def parse(f):
    g = nx.Graph()
    for line in f.read().splitlines():
        l = line.split(':')
        n1 = l[0]
        nodes = l[1].split()
        for n2 in nodes:
            g.add_edge(n1, n2)

    return g


def p1(f):
    g = parse(f)
    # draw_graph(g)
    # for sample
    # g.remove_edge('hfx', 'pzl')
    # g.remove_edge('bvb', 'cmg')
    # g.remove_edge('nvd', 'jqt')
    # for original
    g.remove_edge('pcs', 'rrl')
    g.remove_edge('lcm', 'ddl')
    g.remove_edge('qnd', 'mbk')
    return math.prod(len(c) for c in nx.connected_components(g))


def draw_graph(g):
    nx.draw(g, with_labels=True, node_size=60, font_size=8)
    plt.savefig('./doodles/day25graph.png', dpi=1000)
    plt.show()
