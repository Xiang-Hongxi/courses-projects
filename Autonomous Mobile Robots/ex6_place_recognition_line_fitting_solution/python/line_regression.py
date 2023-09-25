import numpy as np
import matplotlib.pyplot as plt

def load_data(x_path, y_path):
    x=np.load(x_path)
    y=np.load(y_path)
    return x, y

def derive_alpha(x, y, xc, yc):
    # TODO: Implement this function
    alpha = ...
    return alpha

def derive_r(xc, yc, alpha):
    # TODO: Implement this function
    r = ...
    return r

def pol2cart(alpha, r):
    xz = r * np.cos(alpha)
    yz = r * np.sin(alpha)
    return xz, yz

def plot_fit(x, y, alpha, r):
    # Plot the points
    plt.scatter(x, y)

    # Plot the line
    xz, yz = pol2cart(alpha, r)
    line_foot_point = np.array([xz, yz])
    delta_vec = np.array([-np.sin(alpha), np.cos(alpha)]) * 10
    line_points = np.vstack((line_foot_point, line_foot_point + delta_vec))
    plt.plot(line_points[:,0], line_points[:, 1], color='red')

    plt.show()

if __name__ == '__main__':
    # Load test data
    x_path = './x.npy'
    y_path = './y.npy'
    x, y = load_data(x_path, y_path)

    # Compute the centroid
    N = x.shape[0]
    assert (N == y.shape[0])
    xc = np.sum(x) / N
    yc = np.sum(y) / N

    # Part 1: Derive the parameter alpha
    alpha = derive_alpha(x, y, xc, yc)

    # Part 2: Derive the parameter r using alpha
    r = derive_r(xc, yc, alpha)

    print(f'Found line with parameters alpha = {alpha} and r = {r}')

    plot_fit(x, y, alpha, r)
