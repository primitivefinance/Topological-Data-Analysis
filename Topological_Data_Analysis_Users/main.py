from platform import node
from getData import get_data
from buildGraph import build_graph
from visualize import visualize
import networkx as nx


def main():
    users = get_data()
    print(users.head())
    graph = build_graph(users.head())
    visualize(graph)


if __name__ == "__main__":
    main()
