import argparse
import glob
import os

from shortest_path import a_star, dijkstra, dijkstra_multi_target
from utils import (compare_solution_to_gt, read_coords_from_file,
                   read_graph_from_file)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--shortest_path_type",
    type=str,
    choices=["a_star", "dijkstra", "dijkstra_multitarget"],
    required=True,
    help=("Type of shortest-path algorithm to use. Either `a_star`, "
          "`dijkstra`, or `dijkstra_multitarget`."),
)
args = parser.parse_args()

# Iterate over all graphs in the `graphs/` folder.
for graph_file in sorted(glob.glob("graphs/*_graph.txt")):
    # - Read graph and start and target node for the Dijkstra's / A* algorithm.
    adjacency_lists, start_node, target_node = read_graph_from_file(
        file_path=graph_file)
    # - If using A*, read the 2-D coordinates of the nodes in the graph.
    node_coordinates = None
    if (args.shortest_path_type == "a_star"):
        coordinate_file = os.path.join(
            "graphs",
            os.path.basename(graph_file).split("_graph.txt")[0] +
            "_coords.txt")
        assert os.path.exists(coordinate_file), (
            f"The coordinate file '{coordinate_file}' required by A* to "
            "compute the heuristics function (based on the 2-D coordinate of "
            "the nodes) was not found.")
        node_coordinates = read_coords_from_file(file_path=coordinate_file)

    # - Run Dijkstra's / A* algorithm.
    if (args.shortest_path_type == "a_star"):
        shortest_distance, shortest_path = a_star(
            adjacency_lists=adjacency_lists,
            start_node=start_node,
            target_node=target_node,
            node_coordinates=node_coordinates,
        )
        distances_and_shortest_paths = [(shortest_distance, shortest_path)]
    elif (args.shortest_path_type == "dijkstra"):
        shortest_distance, shortest_path = dijkstra(
            adjacency_lists=adjacency_lists,
            start_node=start_node,
            target_node=target_node)
        distances_and_shortest_paths = [(shortest_distance, shortest_path)]
    elif (args.shortest_path_type == "dijkstra_multitarget"):
        distances_and_shortest_paths = dijkstra_multi_target(
            adjacency_lists=adjacency_lists, start_node=start_node)
    # - Compare the solution.
    solution_file = os.path.join(
        "graphs",
        os.path.basename(graph_file).split("_graph.txt")[0] + "_solution.txt")
    print(f"Checking the solution for the graph '{graph_file}'.")
    if (os.path.exists(solution_file)):
        compare_solution_to_gt(
            distances_and_shortest_paths=distances_and_shortest_paths,
            solution_file_path=solution_file,
            adjacency_lists=adjacency_lists)
    else:
        print(
            "\033[93m- The solution cannot be checked because the ground-truth "
            f"file '{solution_file}' was not found.\033[0m")
