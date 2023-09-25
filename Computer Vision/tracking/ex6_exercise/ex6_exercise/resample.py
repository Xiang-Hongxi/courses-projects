import numpy as np

def resample(particles, particles_w):
    num_particles = particles.shape[0]
    sample_indices = np.random.choice(np.arange(num_particles), size=num_particles, replace = True, p = particles_w.flatten())
    new_particles = particles[sample_indices, :]
    new_particles_w = particles_w[sample_indices]
    new_particles_w = new_particles_w/(np.sum(new_particles_w)) # normalize
    new_particles_w = new_particles_w.reshape(particles.shape[0],1)

    return new_particles, new_particles_w


