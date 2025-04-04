#python implementation of the netseer library for R

import sys

from collections.abc import Iterable
import numpy as np
import igraph as ig
import argparse

import generate_graph 
import forecasting
import prediction
import utils

def predict_graph(graph_list : Iterable[ig.Graph], h=5, conf_nodes=None, conf_degree=90, weights_option=4):#5"not_implemented"
    print("Forecasting properties of the new graph")
    #predict the number of nodes for the predicted graph
    new_nodes, new_nodes_lower, new_nodes_upper = forecasting.predict_num_nodes(graph_list, h=h, conf_level=conf_nodes)
    #predict the degrees for the new nodes
    new_nodes_degrees = forecasting.predict_new_nodes_degrees(graph_list)
    
    #predict the degrees of the existing nodes
    existing_nodes_degrees = forecasting.predict_existing_nodes_degrees(graph_list, h=h, conf_level=conf_degree)

    total_edges = forecasting.predict_total_edges_counts(graph_list, h=h, conf_level = conf_degree)

    EDGES_CONF_LEVEL = "conf_high" #"mean"
    print("Using forecasts to predict the new graph")
    mean_graph = prediction.predict_graph_from_forecasts(graph_list, new_nodes, existing_nodes_degrees[EDGES_CONF_LEVEL], new_nodes_degrees, total_edges[EDGES_CONF_LEVEL], conf_nodes, conf_degree, weights_option)

    print("done")
    return mean_graph

def main(*arguments):
    arg_parser = argparse.ArgumentParser("Netseer Network Graph Prediction")
    arg_parser.add_argument("--graph_list", help="Graph list to predict", type=str, nargs="+")
    arg_parser.add_argument("--pickled_list", help="Read a pickled graph list to predict", type=str)
    arg_parser.add_argument("--validate", help="Validate the results for a supplied graph list", action="store_true")
    arg_parser.add_argument("--random_graph", help="Generate a random graph list to predict", action="store_true")
    arg_parser.add_argument("--h", "-n", help="Number of time steps to predict into the future", type=int, default=5)
    arg_parser.add_argument("-o", "--out_filename", help="Save the predicted graph to this location", type=str)

    arg_parser.add_argument("--start_nodes", help="Random graph starting number of nodes", type=int, default=100)
    arg_parser.add_argument("--add_nodes", help="Number of new nodes to add to the random graph each time step", type=int, default=5)
    arg_parser.add_argument("--add_edges", help="Number of new edges to add to the random graph each time step", type=int, default=20)
    arg_parser.add_argument("--remove_edges", help="Number of edges to remove from the random graph each time step", type=int, default=10)
    arg_parser.add_argument("--nn_edges", help="Number of edges that new nodes start with when using a random graph", type=int, default=3)
    arg_parser.add_argument("--num_iters", help="Number of random graphs to produce for the random graph list", type=int, default=15)

    arg_parser.add_argument("--validate_use_graphs", help="Use the first n graphs in the graph list for the validation prediction", type=int, default=-1)
    arg_parser.add_argument("--validate_index", help="Use this index as the actual graph for validation", type=int, default=-1)

    args = arg_parser.parse_args(arguments)

    graph_list = None
    if args.graph_list is not None:
        graph_list = utils.read_graph_list(args.graph_list)
    if args.pickled_list is not None:
        graph_list = utils.read_pickled_list(args.pickled_list)
    if args.random_graph:
        graph_list = generate_graph.generate_graph_list(start_nodes = args.start_nodes, add_nodes = args.add_nodes, add_edges = args.add_edges, rem_edges = args.remove_edges, nn_edges = args.nn_edges, num_iters = args.num_iters)
    if graph_list is None:
        raise ValueError("Need to supply a graph list or request a random graph to predict")
    
    if args.validate:
        validate_actual_index = args.validate_index if args.validate_index > 0 else len(graph_list) - 1
        graph_list_index = args.validate_use_graphs if args.validate_use_graphs > 0 else validate_actual_index - args.h
        args.h = validate_actual_index - graph_list_index
    else:
        graph_list_index = len(graph_list)

    prediction = predict_graph(graph_list[:graph_list_index+1], args.h)
    if args.out_filename is not None:
        print(f"Saving the predicted graph to {args.out_filename}")
        prediction.write(args.out_filename)
    else:
        print("The predicted graph:")
        print(prediction)

    if args.validate:
        evaluation = utils.evaluation(graph_list[validate_actual_index], prediction)
        print(f"evaluation: {evaluation}")
        evaluation2 = utils.eval_metrics2(graph_list[validate_actual_index], prediction)
        print(f"evaluation metrics 2: {evaluation2}")

    return prediction


if __name__ == "__main__":
    main(*sys.argv[1:])