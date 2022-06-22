import networkx as nx
from getData import get_users_nieghbors
import os
from dotenv import load_dotenv


def build_graph(users):
    load_dotenv()
    G = nx.Graph()
    # G.add_node(0, UTM="0x54522da62a15225c95b01bd61ff58b866c50471f")
    for user in users:
        print(user)
        G.add_node(user, attr="user")
        neighbors = get_users_nieghbors(user)
        for neighbor in neighbors:
            if neighbor not in G.nodes():
                if neighbor == os.environ["PRIMITIVE_MANAGER"]:
                    G.add_node(neighbor, attr="primitive")
                    G.add_edge(user, neighbor)
                else:
                    G.add_node(neighbor, attr="neighbor")
                    G.add_edge(user, neighbor)
            else:
                G.add_edge(user, neighbor)
    return G
