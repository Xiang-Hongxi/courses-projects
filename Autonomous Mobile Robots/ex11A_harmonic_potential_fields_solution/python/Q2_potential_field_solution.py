## Autonomous Mobile Robots - Exercise 11 Q2 - Harmonic Potential Fields
import numpy as np
import matplotlib.pyplot as plt
# from scipy.signal import convolve2d        # <- For convolution solution

# 2.1 - Initialisation
# Initialize traversability map
# 1 for traversable, 0 for obstacle
map = np.ones((11, 9))
map[:, [0, -1]] = 0
map[[0, -1], :] = 0
map[4:6, 4:8] = 0
map[8:10, 1] = 0
map[9, 2] = 0

# Initialize search start and goal locations
search_start = [2, 6]
search_goal = [8, 5]

fh, ah = plt.subplots(1, 2)
fh.set_size_inches(8, 5)

ah[0].set_title('Obstacle map')
ah[0].imshow(map, aspect='equal', cmap='gray')
ah[0].plot(search_start[1], search_start[0], 'g^')
ah[0].plot(search_goal[1], search_goal[0], 'ro')

# Initialize iterative search
potential_field = np.zeros_like(map)
potential_field[map == 0] = 1  # set obstacle cells to 1 (high potential)
potential_field[map == 1] = 0.5  # set free cells to 0.5 (mid potential)
potential_field[search_goal[0], search_goal[1]] = 0  # set goal potential

## 2.2 Iterative updates
# Iterative parameters(max iterations, convergence tolerance)
tol = 0.01
maxIter = 50

ah[1].set_title('Potential Field')
h_image = ah[1].imshow(potential_field, aspect='equal', cmap='viridis')

# Iteratively solve the discrete Laplace equation with
# Dirichlet boundary conditions
i = 0
max_change = 1.0

while max_change > tol:
    assert i < maxIter, 'maxIter assert triggered. Aborting.'
    i += 1

    next_potential = potential_field.copy()

    for x in range(map.shape[0]):
        for y in range(map.shape[1]):
            if map[x, y] == 1 and potential_field[x, y] != 0:
                next_potential[x, y] = 0.25 * (potential_field[x - 1, y] +
                                               potential_field[x + 1, y] +
                                               potential_field[x, y - 1] +
                                               potential_field[x, y + 1])

    # Alternative convolution:
    # next_potential = convolve2d(potential_field, np.array([[0, 0.25, 0], [0.25, 0, 0.25], [0, 0.25, 0]]), mode='same', fillvalue=1.0)
    # next_potential[map == 0] = 1
    # next_potential[search_goal[0], search_goal[1]] = 0

    max_change = np.abs(potential_field - next_potential).max()
    potential_field = next_potential

    # Animate
    plt.pause(0.2)
    h_image.set_data(potential_field)

ah[1].plot(search_start[1], search_start[0], 'g^')
ah[1].plot(search_goal[1], search_goal[0], 'ro')

## 2.3 Backtrack solution
# Extract solution path from start to goal
# Construct the path as a list of points, from the start to the goal
# Assume an 8-connected grid

optimal_path = [search_start]
i = 0
while optimal_path[-1] != search_goal:
    assert i < maxIter, 'maxIter assert triggered. Aborting.'
    i += 1

    # extract index corresponding to the minimal value within a 3x3 window
    cx, cy = optimal_path[-1]
    x, y = np.unravel_index(
        np.argmin(potential_field[cx - 1:cx + 2, cy - 1:cy + 2]), (3, 3))
    optimal_path.append([cx + x - 1, cy + y - 1])

ah[1].plot([y for x, y in optimal_path], [x for x, y in optimal_path], 'r-')
plt.show()
