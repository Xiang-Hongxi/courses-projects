import cv2 as cv                        # install by "pip install opencv-python"
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from ex_5_pointFeatures_utils import insertMarker, getPointLists, \
    stitchImages, detectHarrisFeatures

## Autonomous Mobile Robots - Exercise 5 (Image Saliency)

# Q3.4.c) Panorama creation with scaled images
# Now that you have seen, that the Harris corner detection is invariant to
# rotation (in-plane), could we also stitch together the images if the
# right image was scaled? Have a look at the detected corners for the scaled
# right image and compare them with the ones found in the left image.
# If they are not the same, what type of other feature could you use?
lena = cv.imread('lena.jpeg', cv.IMREAD_GRAYSCALE)
left_lena = cv.imread('left_lena.jpg', cv.IMREAD_GRAYSCALE)
right_lena = cv.imread('scaled_lena.jpg', cv.IMREAD_GRAYSCALE)

# TODO: Extract the corners in the left and right image using the Harris
# corner detector.
# SOLUTION:
left_corners = detectHarrisFeatures(left_lena)
right_corners = detectHarrisFeatures(right_lena)

# visualize our detected corners
left_J = cv.cvtColor(left_lena.copy(), cv.COLOR_GRAY2RGB)
left_J = insertMarker(left_J, left_corners)
right_J = cv.cvtColor(right_lena.copy(), cv.COLOR_GRAY2RGB)
right_J = insertMarker(right_J, right_corners, marker_size=7)
fig1c, ax1c = plt.subplots(1, 2,
                           num='Q3.4c Image alignment, scale - Harris corners')
fig1c.set_size_inches(8, 5)
ax1c[0].imshow(left_J, cmap='gray')
ax1c[0].set_title('Left corners marked')
ax1c[1].imshow(right_J, cmap='gray')
ax1c[1].set_title('Right corners marked')

# TODO: Could we also stitch together the images if the right image is scaled?
# SOLUTION: No, since the Harris corner detector is not scale invariant and will
# therefore not detect the same keypoints in the images.

# TODO: If not, what type of other feature could you we use to solve this problem?
# SOLUTION: To solve this problem, one could use any other feature detector that
# is scale invariant.
# One example would be the SIFT detector.
sift = cv.SIFT_create()
left_points, left_features = sift.detectAndCompute(left_lena, None)
right_points, right_features = sift.detectAndCompute(right_lena, None)

# You could try something very similar with ORB features (replace previous
# lines with these). Note that ORB features are binary! This means that the
# matcher also needs to change to use a different distance metric (Hamming)
# orb = cv.ORB_create(nfeatures=200)
# left_points, left_features = orb.detectAndCompute(left_lena, None)
# right_points, right_features = orb.detectAndCompute(right_lena, None)
# bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

# 3. Feature matching
# create feature matcher
bf = cv.BFMatcher(crossCheck=True)
# match features
feature_pairs = bf.match(right_features, left_features)
# Sort them in the order of their distance to extract best matches
feature_pairs = sorted(feature_pairs, key = lambda x:x.distance)
right_matched_points, left_matched_points = getPointLists(feature_pairs, right_points, left_points)

# Let's visualize our matches.
matched_img = cv.drawMatches(right_lena, right_points, left_lena, left_points, feature_pairs[:70], left_lena)
fig3c, ax3c = plt.subplots(num='Q3.4c Image alignment, scale - Feature matches')
ax3c.imshow(matched_img)

# 4. Relative transformation based on feature pairs
# We use only the first best 70 pairs in this case to get a more robust estimate
right_left_transform, inliers = cv.estimateAffinePartial2D(right_matched_points[:70], left_matched_points[:70])

# identity matrix for left to left image transform
left_left_transform = np.eye(3)
left_left_transform = left_left_transform[:2,:]

# Color right image for better visualization
right_lena_color = right_lena.copy()
right_lena_color = cv.applyColorMap(right_lena_color, cv.COLORMAP_AUTUMN)
left_lena_color = left_lena.copy()
left_lena_color = cv.applyColorMap(left_lena_color, cv.COLORMAP_MAGMA)

# 5. Stitch together images and save them in result image called full_lena
img_size = [lena.shape[0], lena.shape[1], 3]         # we overlay color images, therefore our third component is 3 instead of 1
transforms = [left_left_transform, right_left_transform]
images = [left_lena_color, right_lena_color]
full_lena = stitchImages(transforms, images, img_size)

# Let's see our result
fig4c, ax4c = plt.subplots(num='Q3.4c Image alignment, scale - Stitched image')
ax4c.imshow(full_lena)

plt.show()
