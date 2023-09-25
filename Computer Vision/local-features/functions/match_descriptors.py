import numpy as np

def ssd(desc1, desc2):
    '''
    Sum of squared differences
    Inputs:
    - desc1:        - (q1, feature_dim) descriptor for the first image
    - desc2:        - (q2, feature_dim) descriptor for the first image
    Returns:
    - distances:    - (q1, q2) numpy array storing the squared distance
    '''
    assert desc1.shape[1] == desc2.shape[1]
    # TODO: implement this function please

    # for broadcasting
    augmenteddesc1= desc1[:, np.newaxis] 
    # differenceMatrix: (q1,q2,feature_dim) numpy array
    differenceMatrix = augmenteddesc1 - desc2 
    #distances: (q1, q2) numpy array
    distances = np.sum(differenceMatrix**2, axis = 2) 

    return distances

    # raise NotImplementedError

def match_descriptors(desc1, desc2, method = "one_way", ratio_thresh=0.5):
    '''
    Match descriptors
    Inputs:
    - desc1:        - (q1, feature_dim) descriptor for the first image
    - desc2:        - (q2, feature_dim) descriptor for the first image
    Returns:
    - matches:      - (m x 2) numpy array storing the indices of the matches
    '''
    assert desc1.shape[1] == desc2.shape[1]
    distances = ssd(desc1, desc2)
    q1, q2 = desc1.shape[0], desc2.shape[0]
    matches = None
    if method == "one_way": # Query the nearest neighbor for each keypoint in image 1
        # TODO: implement the one-way nearest neighbor matching here

        Indicesindesc1 = np.array(range(q1))
        Indicesindesc2 = np.argmin(distances,axis =1)
        matches = np.vstack((Indicesindesc1,Indicesindesc2)).T

        return matches
        # raise NotImplementedError
    elif method == "mutual":
        # TODO: implement the mutual nearest neighbor matching here

        # match from img1 to img2
        matches_ow1 = match_descriptors(desc1, desc2, "one_way")
        # match from img2 to img1
        matches_ow2 = match_descriptors(desc2, desc1, "one_way")
        matches_ow2 = matches_ow2[:,[1,0]]

        # keep the matches which are valid in both ways, and delete the others 
        remaining = (matches_ow1[:,None] == matches_ow2).all(-1).any(1)
        matches = matches_ow1[remaining]
        
        return matches
        # raise NotImplementedError
    elif method == "ratio":
        # TODO: implement the ratio test matching here

        matches_ow = match_descriptors(desc1, desc2, "one_way")
        #sort the smallest 2 elements
        distances = np.partition(distances,(0,1)) 
        remaining = np.where(((distances[:,0])/(distances[:,1])) < ratio_thresh )
        matches = matches_ow[remaining]
        
        return matches
        # raise NotImplementedError
    else:
        raise NotImplementedError
    return matches

