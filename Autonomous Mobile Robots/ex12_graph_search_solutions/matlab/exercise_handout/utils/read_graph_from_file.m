function [adjacency, start_node, target_node] = read_graph_from_file(file_path)
% Reads a graph from file. The file is assumed to be in the following
% format:
% 
%     N M
%     start_node target_node
%     first_node_edge_1 second_node_edge_1 weight_edge_1
%     first_node_edge_2 second_node_edge_2 weight_edge_2
%     ...
%     first_node_edge_M second_node_edge_M weight_edge_M
% 
% where `N` and `M` are respectively the number of nodes and the number of
% edges in the graph. The graph is assumed to be undirected, and each edge is
% only included once.
% 
% 
% Args:
%     file_path (str): Path to the file.
% 
% Returns:
%     1. Adjacency matrix, only allow >0 edge weights
%     2. Index of the start node.
%     3. Index of the target node.

fileID = fopen(file_path,'r');

% Read number of nodes and edges.
l1 = sscanf(fgetl(fileID), '%d');
N = l1(1);
M = l1(2);

% Read start and target node.
l2 = sscanf(fgetl(fileID), '%d');
start_node = l2(1);
target_node = l2(2);

% Adjacency matrix
adjacency = -ones(N, N);

m = 0;
tline = fgetl(fileID);
while ischar(tline)
    m = m+1;
    l = sscanf(tline, "%f");
    adjacency(l(1)+1, l(2)+1) = l(3);
    adjacency(l(2)+1, l(1)+1) = l(3);
    tline = fgetl(fileID);
end
fclose(fileID);

assert(m == M, 'Graph read error, M=%d, but %d rows found', M, m)

end
