import time
import os
import random
import math
import torch
import numpy as np

# run `pip install scikit-image` to install skimage, if you haven't done so
from skimage import io, color
from skimage.transform import rescale

def distance(x, X):
    # raise NotImplementedError('distance function not implemented!')
    # num = X.shape[0]
    # dist = np.zeros(num)
    # for i in range(num):
    #     dist[i] = torch.norm((X[i].float() - x.float()))
    # dist = torch.from_numpy(dist)
    dist = torch.norm((X.float() - x.float()), dim=1)
    return dist

def distance_batch(x, X):
    # raise NotImplementedError('distance_batch function not implemented!')
    # dist = torch.norm((X.float() - x.float()), dim=1)
    # broadcasting
    d = X.reshape(-1, 1, 3) - X.reshape(1, -1, 3)
    dist = torch.norm(d.float(), dim=2)
    return dist

def gaussian(dist, bandwidth):
    # raise NotImplementedError('gaussian function not implemented!')
    # weight = (1/(bandwidth*(np.sqrt(2*np.pi)))) * np.exp(-(dist/bandwidth)**2/2)
    # dist = dist.cpu()
    # weight = np.exp(-(dist/bandwidth)**2/2)
    # weight = (1/(bandwidth*(np.sqrt(2*np.pi)))) * torch.exp(-(dist/bandwidth)**2/2)
    weight = torch.exp(-(dist/bandwidth)**2/2)
    
    return weight

def update_point(weight, X):
    # raise NotImplementedError('update_point function not implemented!')
    # num = X.shape[0]
    # x = np.zeros((num,3))
    # x = torch.from_numpy(x)
    # for i in range(num):
    #     x[i] = weight[i] * X[i]
    # x = x.sum(dim = 0)
    # return x
    weight = weight/weight.sum()
    x = torch.sum(weight[:, None] *X, dim = 0)
    return x
    



def update_point_batch(weight, X):
     # raise NotImplementedError('update_point_batch function not implemented!')
     weight = weight/(weight.sum(dim=1)[:,None]) # matrix
     X_update = torch.matmul(weight.float(), X.float())
     return X_update



def meanshift_step(X, bandwidth=2.5):
    X_ = X.clone()
    for i, x in enumerate(X):
        dist = distance(x, X)
        weight = gaussian(dist, bandwidth)
        X_[i] = update_point(weight, X)
    return X_

def meanshift_step_batch(X, bandwidth=2.5):
    # raise NotImplementedError('meanshift_step_batch function not implemented!')
    dist = distance_batch(None, X) # no first augument
    weight = gaussian(dist, bandwidth)
    X_update = update_point_batch(weight, X)
    return X_update



def meanshift(X):
    X = X.clone()
    for _ in range(20):
        # X = meanshift_step(X)   # slow implementation
        X = meanshift_step_batch(X)   # fast implementation
    return X

scale = 0.25    # downscale the image to run faster


# Load image and convert it to CIELAB space
image = rescale(io.imread('cow.jpg'), scale, multichannel=True)
image_lab = color.rgb2lab(image)
shape = image_lab.shape # record image shape
image_lab = image_lab.reshape([-1, 3])  # flatten the image

# Run your mean-shift algorithm
t = time.time()
# X = meanshift(torch.from_numpy(image_lab)).detach().cpu().numpy()
# X = meanshift(torch.from_numpy(data).cuda()).detach().cpu().numpy()  # you can use GPU if you have one
X = meanshift(torch.from_numpy(image_lab).cuda()).detach().cpu().numpy()
t = time.time() - t
print ('Elapsed time for mean-shift: {}'.format(t))

# Load label colors and draw labels as an image
colors = np.load('colors.npz')['colors']
colors[colors > 1.0] = 1
colors[colors < 0.0] = 0

centroids, labels = np.unique((X / 4).round(), return_inverse=True, axis=0)

result_image = colors[labels].reshape(shape)
result_image = rescale(result_image, 1 / scale, order=0, multichannel=True)     # resize result image to original resolution
result_image = (result_image * 255).astype(np.uint8)
io.imsave('result.png', result_image)
