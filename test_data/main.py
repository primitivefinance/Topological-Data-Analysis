import buildGraph
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.sparse import csr_matrix
from scipy import sparse
import ODEModel
import pandas as pd
from ripser import ripser
from persim import plot_diagrams

# Main script that runs test dynamics for example graphs.
# # TODO: use the heat flow technique here: https://www.degruyter.com/document/doi/10.1515/phys-2019-0027/html?lang=en or from Crane
# using https://math.stackexchange.com/questions/2507331/what-are-vertex-fields-gradient-and-divergence-on-graphs to compute grads and divs ( can weight vertices too)
# # TODO: compute distances from subsets?

def main():

    # Choose number of users and example network
    seed = 1
    users = 50
    remove = 5 # remove some extra edges

    # Choose some time parameter
    t_start = 0
    t_end = 0.25
    number_of_steps = 1000
    t_span = np.linspace(t_start, t_end, number_of_steps)

    # Get randomly generated directed network
    user_network = buildGraph.directed_growing_network(population=users, seed=seed, remove=remove)
    user_network_edge_list = nx.to_pandas_edgelist(user_network)
    #directed_laplacian = csr_matrix(nx.directed_laplacian_matrix(user_network))
    sparse_user_network = nx.to_scipy_sparse_matrix(user_network)
    directed_laplacian = sparse.csgraph.laplacian(sparse_user_network)

    # Get the undirected version
    undirected_user_network = user_network.to_undirected()
    temp_weighted_distances = dict(nx.all_pairs_dijkstra_path_length(undirected_user_network))
    weighted_distances = np.zeros((users,users))
    for user_idx in range(0,users):
        for user_subidx in range(0,users):
            weighted_distances[user_idx, user_subidx] = temp_weighted_distances[user_idx][user_subidx]

    # TODO: BE MORE RIGOROUS WITH HEAT FLOW DISTANCES
    # Compute distances in directed graph using heat flow
    directed_flow_distances = np.zeros((users, users))
    for source_user in range(0,users):
        assets_0 = np.zeros(users)
        assets_0[source_user] = 1

        # Integrate the equation
        model = lambda y, t : ODEModel.model(y,t,L = directed_laplacian, source = source_user)
        assets = odeint(model, assets_0, t_span)

        # Compute normalized gradient field (which is a function on edges)
        normalized_gradient = np.zeros(user_network_edge_list.shape[0])
        for edge_idx in range(0,user_network_edge_list.shape[0]):
            source = int(user_network_edge_list.iloc[edge_idx]['source'])
            target = int(user_network_edge_list.iloc[edge_idx]['target'])
            weight = user_network_edge_list.iloc[edge_idx]['weight']
            normalized_gradient[edge_idx] = np.sqrt(weight) * (assets[-1][target] - assets[-1][source]) # compute gradient
            # if source_user == users-1:
            #     print(assets[:][-1])
            #     print(source)
            #     print(target)
            #     print(assets[target][-1])
            #     print(assets[source][-1])

        norm = np.linalg.norm(normalized_gradient)
        normalized_gradient = [normalized_gradient[edge_idx] / norm for edge_idx in range(0,user_network_edge_list.shape[0])]

        # Compute divergence of normalized gradient
        divergence = np.zeros(users)
        for edge_idx in range(0,user_network_edge_list.shape[0]):
            source = int(user_network_edge_list.iloc[edge_idx]['source'])
            target = int(user_network_edge_list.iloc[edge_idx]['target'])
            weight = user_network_edge_list.iloc[edge_idx]['weight']
            divergence[source] = divergence[source] + np.sqrt(weight) * normalized_gradient[edge_idx]
            divergence[target] = divergence[target] - np.sqrt(weight) * normalized_gradient[edge_idx]

        eikonal = sparse.linalg.lsqr(directed_laplacian.todense(), np.transpose(divergence))[0]
        # for user in range(0,users):
        #     user_source_connections = user_network_edge_list.loc[user_network_edge_list['source'] == user]
        #     user_sink_connections = user_network_edge_list.loc[user_network_edge_list['source'] == user]
        #     divergence[user] = sum(user_source_connections[]


        directed_flow_distances[source_user][:] = eikonal
        # directed_flow_distances[source_user][:] =  (t_span[-1] - t_span[0]) / (assets[-1][:] - assets[0][:])
        # directed_flow_distances[source_user][source_user] = 0

    #print(directed_laplacian.todense())
    #print(directed_flow_distances)
    #Plot the flow
    # for user in range(0,users-1):
    #     plt.plot(t_span, assets[:,user], label=user)
    #
    # plt.legend()
    # plt.show()

    # Visualize distance heatmaps
    plt.figure(1)
    plt.imshow(directed_flow_distances, cmap='hot', interpolation='nearest')
    plt.show()
    #
    # plt.figure(2)
    # plt.imshow(weighted_distances, cmap='hot', interpolation='nearest')

    # Visualize graph
    # plt.figure(3)
    # pos = nx.spring_layout(undirected_user_network, scale=10*users, k=10/np.sqrt(user_network.order()))
    # nodes , degree = map(list, zip(*list(nx.degree(user_network))))
    # nx.draw_networkx_nodes(user_network, pos) # node_size=[value * 100 for value in degree]
    # nx.draw_networkx_edges(user_network, pos, width=3)
    # nx.draw_networkx_labels(user_network, pos, font_size=20, font_family="sans-serif")
    # edge_labels = nx.get_edge_attributes(user_network, "weight")
    # nx.draw_networkx_edge_labels(user_network, pos, edge_labels)
    # plt.show()
    #
    # # Plot persistence diagrams
    # plt.figure(4)
    # directed_flow_distances = sparse.coo_matrix(directed_flow_distances)
    # results_directed = ripser(directed_flow_distances, distance_matrix = True, maxdim = 2)['dgms']
    # plot_diagrams(results_directed, show = True)
    # #
    # #
    # plt.figure(5)
    # weighted_distances = sparse.coo_matrix(weighted_distances)
    # results_undirected = ripser(weighted_distances, distance_matrix = True, maxdim = 2)['dgms']
    # plot_diagrams(results_undirected, show = True)



if __name__ == "__main__":
    main()
