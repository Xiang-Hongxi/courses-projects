function costs_and_paths = a_star(adjacency_matrix, start_node, target_node, node_coordinates)
%     Runs the A* algorithm on the input graph (represented as
%     adjacency lists), using the Euclidean distance to the
%     target node as heuristics. Returns the shortest distance and the shortest path
%     between the provided start and target nodes. If the 2-D coordinates of each
%     node are not provided, Dijkstra is run instead.
%     If target_node is -1, the shortest distance and the shortest path from
%     `start_node` to all the nodes in the graph are computed instead (ignore heuristic).
% 
%     Args:
%         adjacency_matrix (NxN): Input graph represented as weight matrix (cf.
%             `read_graph_from_file` in `utils`).
%         start_node (int): Index of the start node.
%         target_node (int): Index of the target node. 
%         node_coordinates (Nx2 array): 2-D
%             coordinates associated to each node, to use to compute the
%             heuristics used for the A* algorithm. If not included, can set
%             heuristic to 0 (Dijkstra's algorithm), 
% 
%     Returns:
%         costs_and_paths: cell array with elements of cost and then path sequence
%           {[cost, start_node, ..., target_node]}.

%% IMPLEMENT A-STAR

% A rough guide is provided to start, along with the helper priority queue class in utils

% NOTE: We will use zero-indexing to match the python 0 indexing, so first 
% node is node 0. To make this more matlab-y, we just add one and sort it
% out later
start_node = start_node + 1;
target_node = target_node + 1;

% Get the number of nodes.
N = size(adjacency_matrix, 1);
...


% In case A* should be run, check that the input coordinates are in the
% right format and initialize the heuristics terms.
heuristics_term = zeros(N, 1);

% (Calculate the distances from each node to goal node and store in heuristics_term)

path_found = false;

% Initialise accepted nodes array (row: [cost_of_arrival, best_parent_ID])
accepted_nodes = -ones(N,2);

% Initialize the priority queue with the neighbors of the start node.
% Remember, elements in pq are [priority, node_number, best_parent, cost_of_arrival]
priority_queue = PriorityQueue([0, start_node, start_node, 0]);

while priority_queue.n_rows > 0
    
    % Pop the first element from the priority queue
    cnode = priority_queue.pop();
    ...
    
    % If we have already accepted the current node (in accepted_nodes)
    % move on
    ...

    % Otherwise, add it to the accepted list
    accepted_nodes(current_node,:) = ...
    
    % Check if we're at the goal
    if current_node == target_node
        ...
    end
    
    % Get index of neighbours to current node (where adjacency matrix row >0)
    neighbours = ...
    
    % Check if shorter path found
    for n = neighbours
        
        % Cost to arrive from current node
        c_arrival = ...
        
        % Look up heuristic value for this node
        h = ...

        % Push to priority queue (it handles duplicates internally)
        priority_queue.push([...]);
        
    end    
end


% Extract path/s if found
if path_found    
    % Matlab doesn't like increasing array size, but too bad
    reverse_path = [target_node];
    cost = accepted_nodes(target_node, 1);
    parent_node = accepted_nodes(target_node, 2);
    
    while parent_node ~= start_node
        reverse_path(end+1) = parent_node;
        parent_node = accepted_nodes(parent_node, 2);
    end
    if start_node ~= target_node
        reverse_path(end+1) = start_node;
    end
    
    % Remove matlab indexing and reverse
    forward_path = fliplr(reverse_path - 1) ;
        
    costs_and_paths = {[cost, forward_path]};

else    
    % No path found
    fprintf("No path found.\n")
    
end
