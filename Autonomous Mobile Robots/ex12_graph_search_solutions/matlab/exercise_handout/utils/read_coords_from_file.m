function coords = read_coords_from_file(input_file)
% Reads the 2-D coordinates of the nodes in the graph from a file.
% The file contains `N` lines, where `N` is the number of nodes in the graph.
% The `i`-th line contains two floats, encoding the 2-D coordinates of the
% `i`-th node.
% 
% Args:
%     file_path (str): Path to the file.
% 
% Returns:
%     Coordinates of the nodes in the graph, represented as an array of
%     shape `(N, 2)`.


coords=readmatrix(input_file);

end