function costs_and_paths = dijkstra(adjacency_matrix, start_node, target_node)
%     Runs the Dijkstra's algorithm on the input graph (represented as
%     adjacency lists) and returns the shortest distance and the shortest path
%     between the provided start and target nodes. When using Dijkstra, 
%     `target_node` can be set to -1 in which case the shortest distance and 
%     the shortest path from `start_node` to all the nodes in the graph 
%     is computed instead.
% 
%     Args:
%         adjacency_matrix (NxN): Input graph represented as weight matrix (cf.
%             `read_graph_from_file` in `utils`, element i,j = -1 for no edge i->j).
%         start_node (int): Index of the start node.
%         target_node (int or None): Index of the target node. If -1, the
%             shortest distance and the shortest path from `start_node` to all the
%             nodes in the graph is computed instead.
%         node_coordinates (np.ndarray, default=None): If not `None`, 2-D
%             coordinates associated to each node, to use to compute the
%             heuristics used for the A* algorithm.
% 
%     Returns:
%         1. Length of the shortest path between `start_node` and `target_node`.
%         2. Shortest path between `start_node` and `target_node`, represented as
%            a list in which all the nodes along the path -- including
%            `start_node` and `target_node` -- are listed in order of traversal.
%         If `target_node` is None, a list with `N` elements is returned (where
%         `N` is the number of nodes in the graph) instead, with the `i`-th
%         element being a tuple of the same format described above and with
%         `target_node` equal to `i`.

% We made our A* work so that without an array of locations it uses zero heuristic (Dijkstra)
costs_and_paths = a_star(adjacency_matrix, start_node, target_node);