function costs_and_paths = a_star(adjacency_matrix, start_node, target_node, varargin)
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
%         target_node (int): Index of the target node. If -1, the
%             shortest distance and the shortest path from `start_node` to all the
%             nodes in the graph is computed instead (single-source Dijkstra)
%         node_coordinates (Nx2 array, default=None): If not included, will set
%             heuristic to 0 (Dijkstra's algorithm), 2-D
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

% NOTE: We will use zero-indexing to match the python 0 indexing, so first 
% node is node 0. To make this more matlab-y, we just add one and sort it
% out later
start_node = start_node + 1;
target_node = target_node + 1;

% Get the number of nodes.
N = size(adjacency_matrix, 1);
assert(start_node > 0 && start_node <= N, 'Start node %d outside [0, %d]', start_node-1, N-1 );

assert(target_node >= 0 && target_node <= N, 'Target node %d outside [0, %d]', target_node-1, N-1);

% In case A* should be run, check that the input coordinates are in the
% right format and initialize the heuristics terms.
if target_node ~= 0 && nargin > 4
    % Assume 4th input is node_coordinates
    node_coordinates = varargin{1};
    assert(all(shape(node_coordinates) == [N, 2]), 'Node coordinates must be [n x 2]')
    
    % Calculate L2 distances
    heuristics_term = sqrt(sum((node_coordinates - node_coordinates(target_node+1,:)).^2, 2));
else
    heuristics_term = zeros(N, 1);
end

path_found = false;

% Initialise accepted nodes array (row: [cost_of_arrival, best_parent_ID])
accepted_nodes = -ones(N,2);

% Initialize the priority queue with the neighbors of the start node.
% Remember, elements in pq are [priority, node_number, best_parent, cost_of_arrival]
priority_queue = PriorityQueue([0, start_node, start_node, 0]);

while priority_queue.n_rows > 0
    
    % Pop the first element from the priority queue
    cnode = priority_queue.pop();
    current_node = cnode(2);
    current_cost = cnode(4);
    
    % If we have already accepted it, move on
    if accepted_nodes(current_node, 1) ~= -1
        continue;
    end

    % Otherwise, add it to the accepted list
    accepted_nodes(current_node,:) = [current_cost, cnode(3)];
    
    % Check if we're at the goal
    if current_node == target_node
        path_found = true;
        break;
    end
    
    % Get index of neighbours to current node
    neighbours = find(adjacency_matrix(current_node,:)>0) ;
    
    % Check if shorter path found
    for n = neighbours
        
        % Cost to arrive from current node
        c_arrival = current_cost + adjacency_matrix(current_node, n);
        
        % Push to priority queue (it handles duplicates internally)
        h = heuristics_term(current_node);
        priority_queue.push([c_arrival + h, n, current_node, c_arrival]);
        
    end    
end


% Extract path/s if found
if target_node == 0
    costs_and_paths = cell(N);
    for i = 1:N
        reverse_path = [i];
        cost = accepted_nodes(i, 1);
        parent_node = accepted_nodes(i, 2);
        
        while parent_node ~= start_node
            reverse_path(end+1) = parent_node;
            parent_node = accepted_nodes(parent_node, 2);
        end
        if start_node ~= i
            reverse_path(end+1) = start_node;
        end
    
        
        % Remove matlab indexing and reverse
        forward_path = fliplr(reverse_path - 1) ;
            
        costs_and_paths{i} = [cost, forward_path];
    end
        
elseif path_found    
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
