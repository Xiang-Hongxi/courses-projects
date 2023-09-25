import matplotlib.pyplot as plt
from kf_extras import KFPlot
import numpy as np

time_duration = 50  # [sec]
dT = 0.5            # time steps [sec]
g_moon = 1.62       # m/s2 gravity on the moon
a_thrust = 1.52     # m/s2 thrust of the rocket engines

R = 10.0**2         # Measurement variance (sigma^2)
sigma_v = 0.50      # Standard deviation of velocity noise (iid at each time step)
Q = np.array([[dT**2, dT], [dT, 1]])*sigma_v**2  # Process noise

# If you want to set a consistent random seed, uncomment the following line:
# np.random.seed(1)

# (1) TODO: Fill in state-transition model F, the control-input model B, and observation model H
# Motion Model
# F = ???
# B = ???
# Observation model
# H = 


def motion_model(x,u):
    # (2) TODO: Define the motion model for the spacecraft using state-transition model F and the control-input model B
    # x = ???
    return x


def observation_model(x):
    z = H @ x
    return z


def ground_truth_motion(x, u, t):
    x_true = motion_model(x, u)
    # Because the true motion is noisy, we have to add randomly-sampled process noise ~N(0, Q)
    x_true += np.atleast_2d(np.random.multivariate_normal(np.array([0, 0]), Q)).T
    z = make_observation(x_true, t)  # Make an observation from the new (true) state
    return x_true, z


def make_observation(x, t):
    z = observation_model(x) + np.sqrt(R) * np.random.randn(1)
    return z


def deadreckoning(x, u):
    # Dead reckoning doesn't know about the motion noise, it just assumes
    # the control action was perfect and integrates
    x_deadreckoning = motion_model(x, u)
    return x_deadreckoning


def kalman_filter(x: np.array, P: np.ndarray, u: float, z: float):
    """
    Input variables:
    @x: Filter State
    @P: 2x2 Covariance matrix
    @u: Control Input
    @z: Measurement
    """

    # Prediction Step
    # (3) TODO: Compute the a prior estimate for the filter state and the covariance matrix 
    # x_predicted = ???
    # P_predicted = ???

    # Update Step if a measurement is available
    z_predicted = observation_model(x_predicted)

    # (4) TODO: Compute the Kalman Gain and the posterior for the filter state and covariance matrix
    # y = ???
    # S = ???
    # K = ???
    # x_estimated = ???
    # P_estimated = ???
    return x_estimated, P_estimated


def main():
    # Simulation setup
    n_steps = int(time_duration / dT)
    timestamps = np.zeros(n_steps + 1)
    x_true = np.zeros((len(timestamps), 2, 1))  # True state
    x_deadreckoning = np.zeros_like(x_true)     # Dead reckoning state
    x_estimated = np.zeros_like(x_true)         # KF estimated state
    z = np.zeros_like(timestamps)               # Measurements
    P = np.zeros((n_steps + 1, 2, 2))           # P (state covariance estimate) history

    # Time
    cur_time = 0.0
    timestamps[0] = cur_time

    # Control input
    u = a_thrust - g_moon

    # State at time 0
    x_true[0] = np.array([[150.0], [0]])
    x_deadreckoning[0] = x_true[0] + np.array([[20], [-1]])     # Add an initial offset to the estimated state
    x_estimated[0] = x_deadreckoning[0]
    z[0] = observation_model(x_true[0])
    P[0] = np.diag([10**2, 2**2])            # This is the prior state variance, try changing it to see the effect

    # Make plot
    kf_plot = KFPlot(time_duration, h0=x_true[0][0], R=R)

    for i in range(1, n_steps + 1):
        cur_time += dT
        timestamps[i] = cur_time

        # Ground-truth trajectory without noise
        x_true[i], z[i] = ground_truth_motion(x_true[i - 1], u, cur_time)
        x_deadreckoning[i] = deadreckoning(x_deadreckoning[i - 1], u)
        x_estimated[i], P[i] = kalman_filter(x_estimated[i - 1], P[i - 1], u, z[i])

        if x_true[i][0] <= 0.:
            break

        # Animation
        kf_plot.update(timestamps[:i + 1], x_true[:i + 1], x_deadreckoning[:i + 1], x_estimated[:i + 1], z[:i + 1],
                       P[:i + 1])


if __name__ == "__main__":
    main()
    plt.show()
