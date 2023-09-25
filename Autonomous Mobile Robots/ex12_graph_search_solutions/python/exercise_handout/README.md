# Dijkstra / A* exercise
## Setup
Create a virtualenv and install the required libraries as follows:
```bash
sudo apt-get install python3-venv
python3 -m venv ~/amr_ex12
source ~/amr_ex12/bin/activate
pip install -r requirements.txt
```
## Usage
### File format
The script `find_shortest_path.py` will automatically query your implementation on all the graphs in the [`graphs`](./graphs) folder and compare the solution to the ground truth. It is expected that each graph to test is provided as a `<graph_name>_graphs.txt` file, with the format described in the text of Q3 and in the `read_graph_from_file` function in [`utils.py`](./utils.py), and where `<graph_name>` is a label for the graph (e.g., `example`). Running A* additionally requires a `<graph_name>_coords.txt` file containing the 2-D coordinates of each node in the graph, used to compute the heuristics. The format of this file is explained in the text of Q3 and in the `read_coords_from_file` function in [`utils.py`](./utils.py). Finally, verifying the solution requires a ground-truth file `<graph_name>_solution.txt` in the format described in the `compare_solution_to_gt` function in [`utils.py`](./utils.py).

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
The function to parse the files are already provided to you. You only need to implement the functions in [`shortest_path.py`](./shortest_path.py). To run and verify the solutions, you can use the following commands:
- Dijkstra (Q3.1):
    ```bash
    python find_shortest_path.py --shortest_path_type dijkstra
    ```
- A* (Q3.2):
    ```bash
    python find_shortest_path.py --shortest_path_type a_star
    ```
- Multi-target Dijkstra (Q3.3):
    ```bash
    python find_shortest_path.py --shortest_path_type dijkstra_multitarget
    ```