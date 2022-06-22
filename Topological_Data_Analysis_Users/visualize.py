from cgi import test
import networkx as nx
import matplotlib.pyplot as plt


def visualize(G):
    G = prune_G(G)
    node_colors = color_nodes(G)
    nx.draw(G, with_labels=False, node_color=node_colors, font_weight="bold")
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()


def color_nodes(G):
    color_map = nx.get_node_attributes(G, "attr")
    for key in color_map:
        if color_map[key] == "user":
            color_map[key] = "green"
        if color_map[key] == "neighbor":
            color_map[key] = "blue"
        if color_map[key] == "primitive":
            color_map[key] = "purple"
    return [color_map.get(node) for node in G.nodes()]


def prune_G(G):
    remove = [node for node, degree in dict(G.degree()).items() if degree < 2]
    # print(remove)
    # print(G.degree())
    G.remove_nodes_from(remove)
    # print(G.degree())
    return G
