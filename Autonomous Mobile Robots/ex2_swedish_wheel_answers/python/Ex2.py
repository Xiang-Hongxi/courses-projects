import numpy as np
import matplotlib.pyplot as plt
from plotOmnibot import OmnibotPlotter

# Wheel 1, the far right wheel
alpha1 = ...
beta1 = ...
ell1 = ...

# Wheel 2, the top left wheel
alpha2 = ...
beta2 = ...
ell2 = ...

# Wheel 3, the bottom left wheel
alpha3 = ...
beta3 = ...
ell3 = ...

# The wheel radius
r = ...

# Build the equations for each wheel by plugging in the parameters (1x3 arrays)
J1 = np.array([...])
J2 = np.array([...])
J3 = np.array([...])

# Stack the wheel equations
J = np.array([J1, J2, J3])
R = ...

# Compute the forward differential kinematics matrix, F
F = ...

## Try changing the wheel speeds to see what motions the robot does
numSeconds = 10
dt = 0.1
tt = np.arange(0, numSeconds, dt)

# The speed of the first wheel (rad/s)
phiDot1 = 1.0*np.ones_like(tt)
# The speed of the second wheel (rad/s)
phiDot2 = 0.5*np.ones_like(tt)
# The speed of the third wheel (rad/s)
phiDot3 = 0.25*np.ones_like(tt)

# Stationary rotation (1 full rotations in 10 seconds, i.e. 0.1Hz)
# phiDot1 = ...
# phiDot2 = ...
# phiDot3 = ...

# Linear motion in R_X
# phiDot1 = ...
# phiDot2 = ...
# phiDot3 = ...

# In a circle (no rotation)
# phiDot1 = ...
# phiDot2 = ...
# phiDot3 = ...

# BONUS: In a circle + constant rotation
# phiDot1 = ...
# phiDot2 = ...
# phiDot3 = ...

phiDot = np.array([phiDot1, phiDot2, phiDot3])

omni_animator = OmnibotPlotter(F, phiDot, dt)
an = omni_animator.animation()
plt.show()