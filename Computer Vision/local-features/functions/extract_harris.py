from calendar import c
import numpy as np
import scipy as sc
import scipy.signal 
import cv2 

# Harris corner detector
def extract_harris(img, sigma = 1.0, k = 0.05, thresh = 1e-5):
    '''
    Inputs:
    - img:      (h, w) gray-scaled image
    - sigma:    smoothing Gaussian sigma. suggested values: 0.5, 1.0, 2.0
    - k:        Harris response function constant. suggest interval: (0.04 - 0.06)
    - thresh:   scalar value to threshold corner strength. suggested interval: (1e-6 - 1e-4)
    Returns:
    - corners:  (q, 2) numpy array storing the keypoint positions [x, y]
    - C:     (h, w) numpy array storing the corner strength
    '''
    # Convert to float
    img = img.astype(float) / 255.0

    # Compute image gradients
    # TODO: implement the computation of the image gradients Ix and Iy here.
    # You may refer to scipy.signal.convolve2d for the convolution.
    # Do not forget to use the mode "same" to keep the image size unchanged.

    # Filters to compute gradients
    IxFilter = np.array([[0,0,0],[0.5,0,-0.5],[0,0,0]]) 
    IyFilter = np.array([[0,0.5,0],[0,0,0],[0,-0.5,0]])

    # Gradients per pixel
    Ix = scipy.signal.convolve2d(img, IxFilter, boundary='symm', mode="same") 
    Iy = scipy.signal.convolve2d(img, IyFilter, boundary='symm', mode="same")

    # raise NotImplementedError

    # Compute local auto-correlation matrix
    # TODO: compute the auto-correlation matrix here
    # You may refer to cv2.GaussianBlur for the gaussian filtering (border_type=cv2.BORDER_REPLICATE)
    
    # Per pixel
    Ixx = np.square(Ix)
    Iyy = np.square(Iy)
    Ixy = np.multiply(Ix,Iy)

    # Elements of M
    sumofIxx = cv2.GaussianBlur(Ixx, (0, 0), sigmaX = sigma, sigmaY = sigma, borderType = cv2.BORDER_REPLICATE)
    sumofIyy = cv2.GaussianBlur(Iyy, (0, 0), sigmaX = sigma, sigmaY = sigma, borderType = cv2.BORDER_REPLICATE)
    sumofIxy = cv2.GaussianBlur(Ixy, (0, 0), sigmaX = sigma, sigmaY = sigma, borderType = cv2.BORDER_REPLICATE)

    # raise NotImplementedError

    # Compute Harris response function
    # TODO: compute the Harris response function C here
    
    # Determinant of M 
    DetMatrix =  np.multiply(sumofIxx,sumofIyy) - np.square(sumofIxy)
    # Trace of M
    TraceMatrix = sumofIxx + sumofIyy
    # Harris response per pixel
    C = DetMatrix - k * np.square(TraceMatrix)
    # raise NotImplementedError

    # Detection with threshold
    # TODO: detection and find the corners here
    # For the local maximum check, you may refer to scipy.ndimage.maximum_filter to check a 3x3 neighborhood.

    # TresholdedC = np.maximum(C,thresh)
    # MaxFilteredTresholedC = sc.ndimage.maximum_filter(TresholdedC, size=3)
    # corners = np.asarray(np.where((MaxFilteredTresholedC==TresholdedC) & (TresholdedC > thresh))).T
    
    # Detect Keypoints
    MaxFilteredC = sc.ndimage.maximum_filter(C, size=3)
    corners = np.asarray(np.where((MaxFilteredC==C) & (C > thresh))).T
    corners =corners[:,[1,0]] # change x,y coordinates
    
    # raise NotImplementedError
    return corners, C

