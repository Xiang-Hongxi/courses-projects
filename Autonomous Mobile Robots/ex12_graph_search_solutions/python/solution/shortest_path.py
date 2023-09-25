import heapq
import numpy as np

from typing import List, Optional, Tuple, Union


def dijkstra(adjacency_lists: List, start_node: int,
             target_node: int) -> Tuple[int, List]:
    r"""Runs the Dijkstra's algorithm on the input graph (represented as
    adjacency lists) and returns the shortest distance and the shortest path
    between the provided start and target nodes.

    Args:
        adjacency_lists (list): Input graph represented as adjacency lists (cf.
            `read_graph_from_file` in `utils.py`).
        start_node (int): Index of the start node.
        target_node (int): Index of the target node.

    Returns:
        1. Length of the shortest path between `start_node` and `target_node`.
        2. Shortest path between `start_node` and `target_node`, represented as
           a list in which all the nodes along the path -- including
           `start_node` and `target_node` -- are listed in order of traversal.
    """
    return _find_shortest_path(adjacency_lists=adjacency_lists,
                               start_node=start_node,
                               target_node=target_node,
                               node_coordinates=None)


def dijkstra_multi_target(adjacency_lists: List,
                          start_node: int) -> List[Tuple[int, List]]:
    r"""Runs the Dijkstra's algorithm on the input graph (represented as
    adjacency lists) and returns the shortest distance and the shortest path
    between the provided start and all the nodes in the graph.

    Args:
        adjacency_lists (list): Input graph represented as adjacency lists (cf.
            `read_graph_from_file` in `utils.py`).
        start_node (int): Index of the start node.

    Returns:
        List with `N` elements, where `N` is the number of nodes in the graph.
        The `i`-th element of the list is a tuple containing the following
        elements:
            1. Length of the shortest path between `start_node` and the node
               `i`.
            2. Shortest path between `start_node` and node `i`, represented as
               a list in which all the nodes along the path -- including
               `start_node` and node `i` -- are listed in order of traversal. If
               `start_node` coincides with `i`, then this list should contain a
               single element `start_node`.
    """
    return _find_shortest_path(adjacency_lists=adjacency_lists,
                               start_node=start_node,
                               target_node=None,
                               node_coordinates=None)


def a_star(adjacency_lists: List, start_node: int, target_node: int,
           node_coordinates: np.ndarray) -> Tuple[int, List]:
    r"""Runs the A* algorithm on the input graph (represented as adjacency
    lists) and returns the shortest distance and the shortest path between the
    provided start and target nodes. The 2-D coordinates of each node must be
    provided, and the Euclidean distance between each node and the target node
    is used as heuristics.

    Args:
        adjacency_lists (list): Input graph represented as adjacency lists (cf.
            `read_graph_from_file` in `utils.py`).
        start_node (int): Index of the start node.
        target_node (int): Index of the target node.
        node_coordinates (np.ndarray): 2-D coordinates associated to each node,
            to use to compute the heuristics used for the A* algorithm.

    Returns:
        1. Length of the shortest path between `start_node` and `target_node`.
        2. Shortest path between `start_node` and `target_node`, represented as
           a list in which all the nodes along the path -- including
           `start_node` and `target_node` -- are listed in order of traversal.
    """
    return _find_shortest_path(adjacency_lists=adjacency_lists,
                               start_node=start_node,
                               target_node=target_node,
                               node_coordinates=node_coordinates)


def _find_shortest_path(
    adjacency_lists: List,
    start_node: int,
    target_node: Optional[int],
    node_coordinates: Optional[np.ndarray] = None
) -> Union[Tuple[int, List], List[Tuple[int, List]]]:
    r"""Runs the Dijkstra's algorithm on the input graph (represented as
    adjacency lists) and returns the shortest distance and the shortest path
    between the provided start and target nodes. If the 2-D coordinates of each
    node are provided, A* is run instead, using the Euclidean distance to the
    target node as heuristics. When using Dijkstra, `target_node` can be set to
    `None`, in which case the shortest distance and the shortest path from
    `start_node` to all the nodes in the graph is computed instead.

    Args:
        adjacency_lists (list): Input graph represented as adjacency lists (cf.
            `read_graph_from_file` in `utils.py`).
        start_node (int): Index of the start node.
        target_node (int or None): Index of the target node. If `None`, the
            shortest distance and the shortest path from `start_node` to all the
            nodes in the graph is computed instead.
        node_coordinates (np.ndarray, default=None): If not `None`, 2-D
            coordinates associated to each node, to use to compute the
            heuristics used for the A* algorithm.

    Returns:
        1. Length of the shortest path between `start_node` and `target_node`.
        2. Shortest path between `start_node` and `target_node`, represented as
           a list in which all the nodes along the path -- including
           `start_node` and `target_node` -- are listed in order of traversal.
        If `target_node` is None, a list with `N` elements is returned (where
        `N` is the number of nodes in the graph) instead, with the `i`-th
        element being a tuple of the same format described above and with
        `target_node` equal to `i`.
    """
    # Get the number of nodes.
    N = len(adjacency_lists)
    assert (start_node in range(0, N))
    if (target_node is not None):
        assert (target_node in range(0, N))
    else:
        assert (node_coordinates is None), (
            "Multi-target shortest path is currently only supported with "
            "Dijkstra.")

    # In case A* should be run, check that the input coordinates are in the
    # right format and initialize the heuristics terms.
    if (node_coordinates is not None):
        assert (isinstance(node_coordinates, np.ndarray)
                and node_coordinates.shape == (N, 2))
        heuristics_term = [None for _ in range(N)]
    else:
        heuristics_term = [0.0 for _ in range(N)]

    # Initialize the distances.
    distance = [np.inf for _ in range(N)]
    distance[start_node] = 0.

    # Initialize the parent nodes.
    parent = [None for _ in range(N)]

    # Initialize flags indicating whether a node was ever taken as starting node
    # when popping elements from the priority queue. By principle of optimality,
    # if this happened, then it is not necessary to add any other edges that end
    # in this node to the priority queue.
    was_node_closed = [False for _ in range(N)]
    was_node_closed[start_node] = True

    # Initialize the priority queue with the neighbors of the start node.
    priority_queue = []
    for neighbor, weight in adjacency_lists[start_node]:
        # Add the heuristics term based on the Euclidean distance to
        # the goal if using A* star.
        if (node_coordinates is not None):
            if (heuristics_term[neighbor] is None):
                heuristics_term[neighbor] = np.linalg.norm(
                    node_coordinates[neighbor] - node_coordinates[target_node])
        heapq.heappush(
            priority_queue,
            (weight + heuristics_term[neighbor], start_node, neighbor))

    while (len(priority_queue) > 0):
        new_value_curr_node, parent_node, curr_node = heapq.heappop(
            priority_queue)
        new_distance_curr_node = new_value_curr_node - heuristics_term[
            curr_node]
        was_node_closed[parent_node] = True
        # If a single target node is provided, one can terminate early when the
        # target node gets "closed".
        if (target_node is not None and parent_node == target_node):
            break

        if (distance[curr_node] > new_distance_curr_node):
            # Update the distance to `curr_node`.
            distance[curr_node] = new_distance_curr_node
            # Update the parent.
            parent[curr_node] = parent_node
            # Add the edges if necessary.
            for neighbor, weight_to_neighbor in adjacency_lists[curr_node]:
                if (not was_node_closed[neighbor]):
                    # Add the heuristics term based on the Euclidean distance to
                    # the goal if using A* star.
                    if (node_coordinates is not None):
                        if (heuristics_term[neighbor] is None):
                            heuristics_term[neighbor] = np.linalg.norm(
                                node_coordinates[neighbor] -
                                node_coordinates[target_node])
                    heapq.heappush(
                        priority_queue,
                        (distance[curr_node] + weight_to_neighbor +
                         heuristics_term[neighbor], curr_node, neighbor))

    # Reconstruct the path from start node to goal node(s).
    if (target_node is None):
        target_node = [*range(N)]
    else:
        target_node = [target_node]

    distances_and_shortest_paths = []

    for curr_target_node in target_node:
        shortest_path = []
        curr_node = curr_target_node
        while (curr_node != start_node):
            shortest_path.insert(0, curr_node)
            curr_node = parent[curr_node]
        shortest_path.insert(0, start_node)

        distances_and_shortest_paths.append(
            (distance[curr_target_node], shortest_path))

    if (len(distances_and_shortest_paths) == 1):
        distances_and_shortest_paths = distances_and_shortest_paths[0]

    return distances_and_shortest_paths