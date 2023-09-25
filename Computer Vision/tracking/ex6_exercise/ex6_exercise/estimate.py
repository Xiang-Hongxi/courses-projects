import numpy as np

def estimate(particles, particles_w):
    num_states = particles.shape[1]
    mean_state = []
    for i in range(num_states):
        state_i = particles[:,i]
        mean_state_i = np.sum(state_i * np.transpose(particles_w))
        mean_state.append(mean_state_i)

    mean_state = np.asarray(mean_state)
    return mean_state

    