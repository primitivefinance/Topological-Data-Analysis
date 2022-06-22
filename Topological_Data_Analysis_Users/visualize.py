import networkx as nx
import matplotlib.pyplot as plt


def visualize(graph):
    nx.draw(graph, with_labels=False, font_weight="bold")
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    plt.show()

    A = nx.adjacency_matrix(graph)

    print(A.todense())
