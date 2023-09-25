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
# corner detector
left_corners = ...
right_corners = ...

# visualize our detected corners
left_J = cv.cvtColor(left_lena.copy(), cv.COLOR_GRAY2RGB)
left_J = insertMarker(left_J, left_corners)
right_J = cv.cvtColor(right_lena.copy(), cv.COLOR_GRAY2RGB)
right_J = insertMarker(right_J, right_corners, marker_size = 7)
fig11, ax11 = plt.subplots(num='Left corners marked for scaled right image')
plt.imshow(left_J, cmap='gray')
fig12, ax12 = plt.subplots(num='Right corners marked for scaled right image')
plt.imshow(right_J, cmap='gray')

# TODO: Could we also stitch together the images if the right image is scaled?

# TODO: If not, what type of other feature could you we use to solve this problem?

plt.show()
