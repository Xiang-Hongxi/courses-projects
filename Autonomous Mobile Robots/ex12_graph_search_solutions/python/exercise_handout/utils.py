import numpy as np
from typing import List, Tuple


def read_graph_from_file(file_path: str) -> Tuple[List, int, int]:
    r"""Reads a graph from file. The file is assumed to be in the following
    format:

        N M
        start_node target_node
        first_node_edge_1 second_node_edge_1 weight_edge_1
        first_node_edge_2 second_node_edge_2 weight_edge_2
        ...
        first_node_edge_M second_node_edge_M weight_edge_M

    where `N` and `M` are respectively the number of nodes and the number of
    edges in the graph. The graph is assumed to be undirected, and each edge is
    only included once.


    Args:
        file_path (str): Path to the file.

    Returns:
        1. Graph represented as a list of `N` elements. Each element of the list
           is itself a list, with the `i` element representing the adjacency
           list of the `i` node. Each element of the adjacency lists is a tuple
           `(j, d)`, where if the tuple `(j, d)` is in the `i`-th adjacency
           list, then the nodes `i` and `j` are connected by an edge with weight
           `d`.
        2. Index of the start node.
        3. Index of the target node.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Read number of nodes and edges.
    first_line = lines[0].split()
    N = int(first_line[0])
    M = int(first_line[1])

    # Read start and target node.
    second_line = lines[1].split()
    start_node = int(second_line[0])
    target_node = int(second_line[1])

    # Initialize the adjacency lists.
    adjacency_lists = [[] for _ in range(N)]

    for edge_idx, curr_line in enumerate(lines[2:]):
        # Read the next edge.
        curr_line = curr_line.split()
        node_1 = int(curr_line[0])
        node_2 = int(curr_line[1])
        edge_weight = float(curr_line[2])
        assert (node_1 in range(0, N) and node_2 in range(0, N))
        assert (edge_weight >= 0.)
        # Add the edge to the adjacency matrices.
        adjacency_lists[node_1].append((node_2, edge_weight))
        adjacency_lists[node_2].append((node_1, edge_weight))

    assert (edge_idx == M - 1), edge_idx

    return adjacency_lists, start_node, target_node


def read_coords_from_file(file_path: str) -> np.ndarray:
    r"""Reads the 2-D coordinates of the nodes in the graph from a file.
    The file contains `N` lines, where `N` is the number of nodes in the graph.
    The `i`-th line contains two floats, encoding the 2-D coordinates of the
    `i`-th node.

    Args:
        file_path (str): Path to the file.

    Returns:
        Coordinates of the nodes in the graph, represented of a numpy array of
        shape `(N, 2)`.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    node_coords = []

    for line in lines:
        line = line.split()
        coord_1 = float(line[0])
        coord_2 = float(line[1])
        node_coords.append([coord_1, coord_2])

    return np.array(node_coords)


def compare_solution_to_gt(distances_and_shortest_paths: List,
                           solution_file_path: str,
                           adjacency_lists: List) -> None:
    r"""Compares the solution from the algorithm with the ground-truth read from
    file. The ground-truth file is assumed to be in the following format:

        N
        cost_from_source_node_to_node_1 <path_from_source_node_to_node_1>
        cost_from_source_node_to_node_2 <path_from_source_node_to_node_2>
        ...
        cost_from_source_node_to_node_N <path_from_source_node_to_node_N>

    where `N` is the number of nodes in the graph, and
    <path_from_source_node_to_node_i> contains the node indices -- including the
    source node and the i-th node -- on the shortest path from the source node
    to the i-th node, in order of traversal.

    Args:
        distances_and_shortest_paths (list): Solution provided by the algorithm
            in the form of a list. Cf. outputs of `_find_shortest_path` in
            `shortest_path.py` for the format.
        solution_file_path (str): Path to the ground-truth file.
        adjacency_lists (list): Input graph represented as adjacency lists (cf.
            `read_graph_from_file`).

    Returns:
        None.
    """
    with open(solution_file_path, "r") as f:
        lines = f.readlines()

    # Read number of nodes.
    first_line = lines[0]
    N = int(first_line)

    # `None` here means all nodes.
    node_index_to_compare = None
    if (len(distances_and_shortest_paths) == 1):
        node_index_to_compare = distances_and_shortest_paths[0][1][-1]
    else:
        assert (
            N == len(distances_and_shortest_paths) and len(lines) == N + 1), (
                "Badly formatted solution/ground-truth file. Mismatch in the "
                "number of nodes in the graph.")

    # Read the ground-truth solution and concurrently compare it with the
    # solution returned by the algorithm.
    source_node = None
    solutions_match = True

    for node_idx, (curr_line, curr_node_solution) in enumerate(
            zip(lines[1:], distances_and_shortest_paths)):
        if (node_index_to_compare is not None
                and node_idx != node_index_to_compare):
            continue
        curr_line = curr_line.split()
        gt_cost_to_curr_node = float(curr_line[0])
        gt_path_to_curr_node = [
            int(node_on_path_idx) for node_on_path_idx in curr_line[1:]
        ]
        cost_to_curr_node = curr_node_solution[0]
        path_to_curr_node = curr_node_solution[1]

        if (source_node is None):
            source_node = gt_path_to_curr_node[0]
        assert (
            path_to_curr_node[0] == gt_path_to_curr_node[0] == source_node
            and path_to_curr_node[-1] == gt_path_to_curr_node[-1] == node_idx
        ), ("Badly formatted solution/ground-truth file. The `i`-th path in "
            "the solution should start from the source node (which needs to be "
            "the same for all paths) and end in the `i`-th node.")

        if (not np.isclose(cost_to_curr_node, gt_cost_to_curr_node)):
            assert (cost_to_curr_node > gt_cost_to_curr_node)
            print("\033[93m- Found a mismatch for the length of the shortest "
                  f"path between the source node and node no. {node_idx}. "
                  f"The ground-truth length is {gt_cost_to_curr_node}, while "
                  f"{cost_to_curr_node} was returned.\033[0m")
            solutions_match = False
        if (path_to_curr_node != gt_path_to_curr_node):
            assert (path_exists_in_graph(adjacency_lists=adjacency_lists,
                                         path=gt_path_to_curr_node))
            if (path_exists_in_graph(adjacency_lists=adjacency_lists,
                                     path=path_to_curr_node)):
                print(
                    "\033[92m- The returned path between the source node and "
                    f"node no. {node_idx} ({path_to_curr_node}) differs from "
                    f"the ground-truth path ({gt_path_to_curr_node}), but is "
                    "also a valid shortest path, with cost "
                    f"{cost_to_curr_node}.\033[0m")
            else:
                print(
                    "\033[91m- The returned path between the source node and "
                    f"node no. {node_idx} ({path_to_curr_node}) does not exist "
                    "in the graph.\033[0m")
            solutions_match = False

    if (solutions_match):
        print("\033[92m- The two solutions match.\033[0m")


def path_exists_in_graph(adjacency_lists: List, path: List) -> bool:
    r"""Checks whether a given path exists in the graph.

    Args:
        adjacency_lists (list): Input graph represented as adjacency lists (cf.
            `read_graph_from_file`).
        path (list): Path of which to check the existence, represented as a list
            of the indices of all nodes in the path, in order of traversal.

    Returns:
        Whether the given path exists in the graph.
    """

    curr_node = path[0]
    for next_node in path[1:]:
        # - Find next node in the adjacency list of the current node.
        found_next_node = False
        for neighboring_nodes_with_cost in adjacency_lists[curr_node]:
            neighboring_node, _ = neighboring_nodes_with_cost
            if (neighboring_node == next_node):
                found_next_node = True
                break
        if (not found_next_node):
            return False
        curr_node = next_node

    return True
