import heapq
import numpy as np

from typing import List, Optional, Tuple


def dijkstra(
    adjacency_lists: List, start_node: int, target_node: int
) -> Tuple[int, List]:
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
    # Q3.1.
    raise NotImplementedError("Implement this function!")


def _find_shortest_path(
    adjacency_lists: List,
    start_node: int,
    target_node: int,
    node_coordinates: Optional[np.ndarray] = None,
) -> Tuple[int, List]:
    r"""Runs the Dijkstra's algorithm on the input graph (represented as
    adjacency lists) and returns the shortest distance and the shortest path
    between the provided start and target nodes. If the 2-D coordinates of each
    node are provided, A* is run instead, using the Euclidean distance to the
    target node as heuristics.

    Args:
        adjacency_lists (list): Input graph represented as adjacency lists (cf.
            `read_graph_from_file` in `utils.py`).
        start_node (int): Index of the start node.
        target_node (int): Index of the target node.
        node_coordinates (np.ndarray, default=None): If not `None`, 2-D
            coordinates associated to each node, to use to compute the
            heuristics used for the A* algorithm.

    Returns:
        1. Length of the shortest path between `start_node` and `target_node`.
        2. Shortest path between `start_node` and `target_node`, represented as
           a list in which all the nodes along the path -- including
           `start_node` and `target_node` -- are listed in order of traversal.
    """
    # Q3.2. Advice: First implement `dijkstra`, then adapt it to also take
    # `node_coordinates` as inputs. You could then replace the body of
    # `dijkstra` with:
    # return _find_shortest_path(adjacency_lists=adjacency_lists,
    #                            start_node=start_node,
    #                            target_node=target_node,
    #                            node_coordinates=None)
    raise NotImplementedError("Implement this function!")


def a_star(
    adjacency_lists: List,
    start_node: int,
    target_node: int,
    node_coordinates: np.ndarray,
) -> Tuple[int, List]:
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
    return _find_shortest_path(
        adjacency_lists=adjacency_lists,
        start_node=start_node,
        target_node=target_node,
        node_coordinates=node_coordinates,
    )


def dijkstra_multi_target(
    adjacency_lists: List, start_node: int
) -> List[Tuple[int, List]]:
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
    # Q3.3. You may adapt `find_shortest_path` to return the set of distances
    # and the shortest paths from `start_node` to all nodes, in the case in
    # which Dijkstra is used (i.e., when `node_coordinates` is None).
    raise NotImplementedError("Implement this function!")
