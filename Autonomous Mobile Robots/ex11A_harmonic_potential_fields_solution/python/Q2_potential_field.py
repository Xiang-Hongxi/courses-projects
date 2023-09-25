## Autonomous Mobile Robots - Exercise 11 Q2 - Harmonic Potential Fields
import numpy as np
import matplotlib.pyplot as plt

# 2.1 - Initialisation
# Initialize traversability map
# 1 for traversable, 0 for obstacle
map = np.array(...)

# Initialize search start and goal locations
search_start = ...
search_goal = ...

fh, ah = plt.subplots(1, 2)
fh.set_size_inches(8, 6)

ah[0].set_title('Obstacle map')
ah[0].imshow(map, aspect='equal', cmap='gray')
ah[0].plot(search_start[1], search_start[0], 'g^')
ah[0].plot(search_goal[1], search_goal[0], 'ro')

# Initialize iterative search
# Set obstacle cells to high potential, goal to low potential
potential_field = ...

## 2.2 Iterative updates
# Iterative parameters(max iterations, convergence tolerance)
tol = 0.01
max_iter = 50

ah[1].set_title('Potential Field')
h_image = ah[1].imshow(potential_field, aspect='equal', cmap='viridis')

# Iteratively solve the discrete Laplace equation with
# Dirichlet boundary conditions
i = 0
max_change = 1.0

while max_change > tol:
    assert i < max_iter, 'max_iter assert triggered. Aborting.'
    i += 1

    # Your iterative update loop here
    # You can overwrite potential_field during each loop, but be careful!
    # The update rule is a function of the old potential values, so if you
    # update in-place, you could encounter issues!
    ...

    # Simple animation
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
    assert i < max_iter, 'maxIter assert triggered. Aborting.'
    i += 1

    # extract index corresponding to the minimal value within a 3x3 window
    next_point = ...
    optimal_path.append(next_point)

ah[1].plot([y for x, y in optimal_path], [x for x, y in optimal_path], 'r-')
plt.show()
