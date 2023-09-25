function costs_and_paths = dijkstra(adjacency_matrix, start_node, target_node)
%     Runs Dijkstra's algorithm on the input graph (represented as
%     adjacency matrix) and returns the shortest distance and the shortest path
%     between the provided start and target nodes. 
% 
%     Args:
%         adjacency_matrix (NxN): Input graph represented as weight matrix (cf.
%             `read_graph_from_file` in `utils`, element i,j = -1 for no edge i->j).
%         start_node (int): Index of the start node.
%         target_node (int): Index of the target node. 
% 
%     Returns:
%         costs_and_paths: cell array with elements of cost and then path sequence
%           {[cost, start_node, ..., target_node]}..

% We made our A* work so that without an array of locations it uses zero heuristic (Dijkstra)


%% IMPLEMENT DIJKSTRA'S ALGORITHM
% A basic structure is given in the a_star function. In fact, it might be easier
% to implement A* and treat Dijkstra as a special case (heuristic = 0).
