from platform import node
from getData import get_data
from buildGraph import build_graph
from visualize import visualize
import networkx as nx


def main():
    users = get_data()
    print(users.head())
    graph = build_graph(users.head())
    # color_map = nx.get_node_attributes(graph, "attr")
    # for key in color_map:
    #     if color_map[key] == "user":
    #         color_map[key] = "green"
    #     if color_map[key] == "neighbor":
    #         color_map[key] = "blue"
    #     if color_map[key] == "primitive":
    #         color_map[key] = "purple"
    # node_colors = [color_map.get(node) for node in graph.nodes()]
    visualize(graph)


if __name__ == "__main__":
    main()
