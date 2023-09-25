import numpy as np
import matplotlib.pyplot as plt
from plotOmnibot import OmnibotPlotter

# Wheel 1, the far right wheel
alpha1 = 0.0
beta1 = 0.0
ell1 = 0.5

# Wheel 2, the top left wheel
alpha2 = (2/3)*np.pi
beta2 = 0.0
ell2 = 0.5

# Wheel 3, the bottom left wheel
alpha3 = (4/3)*np.pi
beta3 = 0.0
ell3 = 0.5

# The wheel radius
r = 0.1

# Build the equations for each wheel by plugging in the parameters
J1 = np.array([np.sin(alpha1+beta1), -np.cos(alpha1+beta1), -ell1*np.cos(beta1)])
J2 = np.array([np.sin(alpha2+beta2), -np.cos(alpha2+beta2), -ell2*np.cos(beta2)])
J3 = np.array([np.sin(alpha3+beta3), -np.cos(alpha3+beta3), -ell3*np.cos(beta3)])

# Stack the wheel equations
J = np.array([J1, J2, J3])
R = r * np.eye(3)

# Compute the forward differential kinematics matrix, F
F = np.linalg.inv(J) @ R

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
# phiDot1 = -2*np.pi*ell1/(r*numSeconds)*np.ones_like(tt)
# phiDot2 = phiDot1
# phiDot3 = phiDot1

# Linear motion in R_X
# phiDot1 = 0*np.ones_like(tt)
# phiDot2 = 0.5*np.ones_like(tt)
# phiDot3 = -phiDot2

# In a circle (no rotation)
# phiDot1 = np.cos(2*np.pi*tt/numSeconds)
# phiDot2 = np.cos(2*np.pi*tt/numSeconds-alpha2)
# phiDot3 = np.cos(2*np.pi*tt/numSeconds-alpha3)

# BONUS: In a circle + constant rotation
# phiDot1 = np.cos(2*np.pi*tt/numSeconds - alpha1) - 2*np.pi*ell1/(r*numSeconds)
# phiDot2 = np.cos(2*np.pi*tt/numSeconds - alpha2) - 2*np.pi*ell1/(r*numSeconds)
# phiDot3 = np.cos(2*np.pi*tt/numSeconds - alpha3) - 2*np.pi*ell1/(r*numSeconds)


phiDot = np.array([phiDot1, phiDot2, phiDot3])

omni_animator = OmnibotPlotter(F, phiDot, dt)
an = omni_animator.animation()
plt.show()