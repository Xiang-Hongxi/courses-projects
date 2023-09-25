# Dijkstra / A* exercise

## Usage
### File format
The scripts `Q3X_[method].m` will automatically query your implementation on all the graphs in the [`graphs`](./graphs) folder and compare the solution to the ground truth. It is expected that each graph to test is provided as a `<graph_name>_graphs.txt` file, with the format described in the text of Q3 and in the `read_graph_from_file` function in [`utils`](./utils), and where `<graph_name>` is a label for the graph (e.g., `example`). Running A* additionally requires a `<graph_name>_coords.txt` file containing the 2-D coordinates of each node in the graph, used to compute the heuristics. The format of this file is explained in the text of Q3 and in the `read_coords_from_file` function in [`utils`](./utils). Finally, verifying the solution requires a ground-truth file `<graph_name>_solution.txt` in the format described in the `compare_solution_to_gt` function in [`utils`](./utils).

*Example graph*:
- File `example_graph.txt`:
    ```
    4 4
    0 3
    0 1 3
    0 2 2
    1 3 3
    2 3 7
    ```
- File `example_coords.txt`:
    ```
    3.0 2.0
    1.0 -1.0
    1.0 3.0
    3.0 -1.0
    ```
- File `example_solution.txt`:
    ```
    4
    0.0 0
    3.0 0 1
    2.0 0 2
    6.0 0 1 3
    ```

### Running the algorithms and verifying the solution
The functions to parse the files are already provided to you. You only need to implement the functions in [`dijkstra.m`](./dijkstra.m), [`a_star.m`](./a_star.m), and [`dijkstra_multi_target.m`](./dijkstra_multi_target.m). To run and verify the solutions, you can use the following commands:
- Dijkstra (Q3.1):
    ```
    matlab Q31_Dijkstra.m
    ```
- A* (Q3.2):
    ```
    matlab Q32_AStar.m
    ```
- Multi-target Dijkstra (Q3.3):
    ```
    matlab Q32_DijkstraMulti.m

*HINT:* We recommend creating one version that can run any of these algorithms with different options. Remember that Dijkstra's algorithm is simply A* with the zero heuristic. The multi target is Dijkstra with no goal node (run until the priority queue is empty).
    ```
