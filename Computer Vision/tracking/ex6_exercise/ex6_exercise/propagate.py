import numpy as np

def propagate(particles, frame_height, frame_width, params):

    # compute matrix A
    if(params["model"] == 0):
        # s = {x,y}
        num_states = 2
        A = np.eye(num_states)
    else:
        # s = {x,y,x_dot,y_dot}
        num_states = 4
        A = np.eye(num_states)
        A[0][2] = 1
        A[1][3] = 1
    

    # draw random noise
    if (params["model"] == 0):
        mean = np.array([0,0])
        std = np.array([params["sigma_position"],params["sigma_position"]])
        noise = np.random.normal(mean, std, particles.shape) # same size as particles: (num_particles, num_states)
    else: 
        mean = np.array([0,0,0,0])
        std = np.array([params["sigma_position"],params["sigma_position"],params["sigma_velocity"],params["sigma_velocity"]])
        noise = np.random.normal(mean, std, particles.shape) # same size as particles: (num_particles, num_states)

    # propagate
    propagated_particles = np.transpose(np.matmul(A, np.transpose(particles)) + np.transpose(noise)) # (num_particles, num_states)
    
    # make sure particles are within frame
    particles_x = propagated_particles[:,0]
    propagated_particles[:,0] = np.clip(particles_x,0,frame_width)
    particles_y = propagated_particles[:,1]
    propagated_particles[:,1] = np.clip(particles_y,0,frame_height)
    return propagated_particles


    
    
    