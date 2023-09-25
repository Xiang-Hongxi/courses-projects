import os
import numpy as np
from datetime import datetime


def main():
    num_nodes = 1000
    num_edges_per_node_range = (1, 4)
    cost_penalty_range = (0.5, 4)
    domain_size = 20
    select_neighbors_from_last_n = 10

    nodes = list()
    edges = list()

    # Add goal node manually.
    nodes.append(np.array([0.5, 4.8]))
    goal_node_index = 0

    for i in range(num_nodes - 1):
        # Sample location.
        coords = (np.random.rand(2) - 0.5) * domain_size

        # Find neighbors.
        num_neighbors = min(
            len(nodes),
            np.random.randint(num_edges_per_node_range[0], num_edges_per_node_range[1]),
        )
        lowest_index = max(0, len(nodes) - select_neighbors_from_last_n)
        select_from = list(range(lowest_index, len(nodes)))
        neighbor_indices = np.random.choice(
            select_from, size=num_neighbors, replace=False
        )

        # Add node.
        new_node_index = len(nodes)
        nodes.append(coords)

        # Add edges.
        for neighbor_index in neighbor_indices:
            # Determine edge weight.
            heuristic_new = np.linalg.norm(nodes[0] - nodes[-1])
            heuristic_neighbor = np.linalg.norm(nodes[0] - nodes[neighbor_index])
            edge_cost_lower_bound = np.abs(heuristic_new - heuristic_neighbor)
            edge_cost = int(
                np.ceil(
                    edge_cost_lower_bound
                    + np.random.uniform(cost_penalty_range[0], cost_penalty_range[1])
                )
            )
            edges.append((new_node_index, neighbor_index, edge_cost))
    start_node_index = len(nodes) - 1

    out_dir = "random_graphs"
    os.makedirs(out_dir, exist_ok=True)
    timestring = datetime.now().strftime("%y%m%d%H%M%S")
    filename = f"{timestring}_n{num_nodes}"

    plot = True
    if plot:
        import networkx as nx
        from matplotlib import pyplot as plt

        G = nx.Graph()
        for i in range(len(nodes)):
            G.add_node(i, pos=tuple(nodes[i]))
        for edge in edges:
            G.add_edge(edge[0], edge[1])
        pos = nx.get_node_attributes(G, "pos")
        nx.draw(G, pos, with_labels=True)
        # plt.show()
        plot_filename = os.path.join(out_dir, f"{filename}_plot.png")
        plt.savefig(plot_filename)

    # Write to file.
    graph_filename = os.path.join(out_dir, f"{filename}_graph.txt")
    coords_filename = os.path.join(out_dir, f"{filename}_coords.txt")

    with open(graph_filename, "w") as f:
        f.write(f"{len(nodes)} {len(edges)}\n")
        f.write(f"{start_node_index} {goal_node_index}\n")
        for edge in edges:
            f.write(f"{edge[0]} {edge[1]} {edge[2]}\n")

    with open(coords_filename, "w") as f:
        for node in nodes:
            f.write(f"{node[0]} {node[1]}\n")


if __name__ == "__main__":
    main()
