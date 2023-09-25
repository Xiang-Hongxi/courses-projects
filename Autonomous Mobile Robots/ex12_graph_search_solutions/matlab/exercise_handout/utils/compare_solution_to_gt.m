function compare_solution_to_gt(distances_and_shortest_paths, solution_file_path, adjacency)
% Compares the solution from the algorithm with the ground-truth read from
% file. The ground-truth file is assumed to be in the following format:
% 
%     N
%     cost_from_source_node_to_node_1 <path_from_source_node_to_node_1>
%     cost_from_source_node_to_node_2 <path_from_source_node_to_node_2>
%     ...
%     cost_from_source_node_to_node_N <path_from_source_node_to_node_N>
% 
% where `N` is the number of nodes in the graph, and
% <path_from_source_node_to_node_i> contains the node indices -- including the
% source node and the i-th node -- on the shortest path from the source node
% to the i-th node, in order of traversal.
% 
% Args:
%     distances_and_shortest_paths (cell array): Solution provided by the algorithm
%         in the form of a list. Cf. outputs of `_find_shortest_path` in
%         `shortest_path.py` for the format.
%     solution_file_path (str): Path to the ground-truth file.
%     adjacency_lists (list): Input graph represented as adjacency lists (cf.
%         `read_graph_from_file`).
% 
% Returns:
%     None.


fileID = fopen(solution_file_path,'r');

% Read number of nodes.
N = sscanf(fgetl(fileID), '%d');

%  -1 here means all nodes.
% node_index_to_compare = -1
% if (length(distances_and_shortest_paths) == 1)
%     node_index_to_compare = distances_and_shortest_paths{1}[1][-1]
% else:
%     assert (
%         N == len(distances_and_shortest_paths) and len(lines) == N + 1), (
%             "Badly formatted solution/ground-truth file. Mismatch in the "
%             "number of nodes in the graph.")

tol = 1e-5;

% Read the ground-truth solution and concurrently compare it with the
% solution returned by the algorithm.
source_node = distances_and_shortest_paths{1}(2);
solutions_match = 1;

m = 1;
cost = distances_and_shortest_paths{m}(1);
path = distances_and_shortest_paths{m}(2:end);

tline = fgetl(fileID);
while ischar(tline)
    % Get each line, and check if our current path is this one
    
    l = sscanf(tline, "%f");
    gt_cost = l(1);
    gt_path = l(2:end);
    
    if source_node ~= gt_path(1) || source_node ~= path(1)
        fprintf('Source node %d does not match for path %d\n', source_node, m);
        solutions_match = 0;
        break
    end
    
    % Is this the path we're looking for?
    if path(end) ~= gt_path(end)
        % Nope? Go to the next one in the file
        tline = fgetl(fileID);
        continue
    end

    % Yes? Check if it's correct
    if abs(gt_cost - cost) > tol
        fprinf('Path lengths do not match for path %d\n', m);
        solutions_match = 0;
        break
    end
    
    % Check that the path is valid and has correct cost
    ccost = 0;
    for i = 1:(length(path)-1)
        edge_cost = adjacency(path(i)+1, path(i+1)+1);
        if edge_cost > 0
            ccost = ccost + edge_cost;
        else
            fprintf('Path %d not a valid path - no edge %d %d\n', m, path(i), path(i+1));
            solutions_match = 0;
            break
        end
    end
    
    if abs(ccost-cost) > tol
        fprintf("Path %d not a valid path, cost doesn't match\n", m);
    end
       
    if ~solutions_match
        break
    end
        
    % Go to next path to check
    if m+1 > length(distances_and_shortest_paths)
        % Have we checked all the paths?
        break
    end
    m = m+1;
    cost = distances_and_shortest_paths{m}(1);
    path = distances_and_shortest_paths{m}(2:end);
    tline = fgetl(fileID);
end
    
fclose(fileID);

if m >1 && N ~= m
    fprintf('Number of paths do not match\n');
    solutions_match = 0;
end

if solutions_match
    fprintf("The two solutions match.\n");
end

end