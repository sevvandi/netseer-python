import random
import numpy as np
import igraph as ig

import utils

gen = np.random.default_rng()

def generate_next_graph(gr : ig.Graph, add_nodes = 50, add_edges = 200, rem_edges = 100, new_node_edges = 3) -> ig.Graph:
    #create a new graph that grows and/or shrinks relative to a previous graph
    gr = gr.copy()
    #remove edges
    edges_to_delete = gen.choice(gr.ecount(), min(rem_edges, gr.ecount()), replace=False)
    gr.delete_edges(edges_to_delete)

    #add edges
    non = utils.get_neighbours_of_neighbours(gr)
    edges_to_add = non[gen.choice(non.shape[0], min(add_edges, non.shape[0]), replace=False)]
    gr.add_edges(edges_to_add)

    #add new nodes
    gr = gr.simplify()
    original_nodes_count = gr.vcount()
    degrees = gr.degree()
    probabilities = np.array(degrees) / sum(degrees)
    gr.add_vertices(n=add_nodes)

    #add edges to new nodes
    total_new_node_edges = new_node_edges * add_nodes
    new_node_ids = np.arange(original_nodes_count, gr.vcount())
    new_edge_starts = gen.choice(original_nodes_count, total_new_node_edges, replace=True, p=probabilities)
    new_edge_ends = gen.choice(new_node_ids, total_new_node_edges, replace=True)
    new_node_edges = np.vstack((new_edge_starts, new_edge_ends)).T
    gr.add_edges(new_node_edges)

    return gr.simplify()


def generate_graph_list(start_nodes = 1000, add_nodes = 50, add_edges = 200, rem_edges = 100, nn_edges = 3, num_iters = 15, mode="linear") -> list[ig.Graph]:
    #randomly generate a list of graphs
    graph_list = [None]*num_iters
    initial_graph = ig.Graph.Barabasi(n=start_nodes, directed=False)
    graph_list[0] = initial_graph
    for i in range(1, num_iters):
        graph_list[i] = generate_next_graph(graph_list[i-1], add_nodes, add_edges, rem_edges, nn_edges)
    return graph_list