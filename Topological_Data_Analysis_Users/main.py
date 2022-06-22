from pprint import pprint
from getData import get_data, get_users_nieghbors
from buildGraph import build_graph
from visualize import visualize


def main():
    users = get_data()
    print(users)
    graph = build_graph(users.head())
    visualize(graph)


if __name__ == "__main__":
    main()
