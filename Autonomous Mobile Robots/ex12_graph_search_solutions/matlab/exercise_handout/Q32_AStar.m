%% Autonomous Mobile Robots - Exercise 12 (Graph Search) - 3.2 A*
close all;
clear all;
clc;
addpath('./utils');

% Iterate over all graphs in the `graphs/` folder.
graphs_dir = './graphs';
graph_files = dir(fullfile(graphs_dir,'*_graph.txt'));

costs_and_paths = {};

for k = 1:length(graph_files)
    baseFileName = graph_files(k).name;
    fullFileName = fullfile(graphs_dir, baseFileName);
    base_graph_name = baseFileName(1:end-10);       % cut off '_graph.txt'

    % - Read graph and start and target node for the Dijkstra's / A* algorithm.
    [adjacency, start_node, target_node] = read_graph_from_file(fullFileName);

    % - Read the 2-D coordinates of the nodes in the graph.
    coordinate_file = fullfile(graphs_dir, strcat(base_graph_name, "_coords.txt"));
    assert(isfile(coordinate_file), "Coordinate file %s required by A* not found.", coordinate_file);
    node_coordinates = read_coords_from_file(coordinate_file);

    % - Run A* algorithm.
    costs_and_paths = a_star(adjacency, start_node, target_node, node_coordinates);

    % Note: costs_and_paths should be a cell array. For A* it should
    % only contain one element, an array containing the path cost and route string
    % for the optimal path on the graph from start_node to target_node, i.e.:
    % costs_and_paths = {[cost, start_node, ..., target_node]}.
    
    % - Compare the solution.
    solution_file = fullfile(graphs_dir, strcat(base_graph_name, "_solution.txt"));
    fprintf("Checking the solution for the graph %s.\n", base_graph_name);
    if isfile(solution_file)
        compare_solution_to_gt(costs_and_paths, solution_file, adjacency);
    else
        fprintf("The solution cannot be checked because the ground-truth\n");
        fprintf("file %s was not found.", solution_file);
    end
end
