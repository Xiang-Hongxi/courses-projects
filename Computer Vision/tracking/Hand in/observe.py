from color_histogram import color_histogram
from chi2_cost import chi2_cost
import numpy as np

def observe(particles, frame, bbox_height, bbox_width, hist_bin, hist, sigma_observe):

    particles_w = []

    for i in range(particles.shape[0]):
        xmin = np.int32(np.max([np.floor(particles[i][0] - bbox_width/2), 0]))
        xmax = np.int32(np.min([xmin + bbox_width, (frame.shape[1]-1)]))
        ymin = np.int32(np.max([np.floor(particles[i][1] - bbox_height/2), 0]))
        ymax = np.int32(np.min([ymin + bbox_height, (frame.shape[0]-1)]))
        hist_x = color_histogram(xmin, ymin, xmax, ymax, frame, hist_bin)
        dist = chi2_cost(hist_x, hist)
        pi_i = 1/(np.sqrt(2*np.pi)*sigma_observe) * np.exp(-(dist**2)/(2*(sigma_observe**2)))
        particles_w.append(pi_i)
    

    particles_w = np.asarray(particles_w)
    particles_w = particles_w/(np.sum(particles_w)) # normalize
    particles_w = particles_w.reshape(particles.shape[0],1)

    return particles_w

    