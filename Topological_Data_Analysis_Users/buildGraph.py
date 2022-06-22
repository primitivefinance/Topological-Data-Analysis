import networkx as nx
from getData import get_users_nieghbors


def build_graph(users):
    G = nx.Graph()
    G.add_nodes_from(users)
    # G.add_node(0, UTM="0x54522da62a15225c95b01bd61ff58b866c50471f")
    for user in users:
        print(user)
        neighbors = get_users_nieghbors(user)
        for neighbor in neighbors:
            G.add_edge(user, neighbor)
    return G
