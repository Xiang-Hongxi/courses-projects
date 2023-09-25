import numpy as np
import matplotlib.pyplot as plt
import Ex1_extras

#############################
####### QUESTION 1 ##########
#############################
# write down the rotation matrices as functions of alpha, beta, gamma
def R_B1(alpha):
        return np.array([[ ..., ..., ... ],
                         [ ..., ..., ... ],
                         [ ..., ..., ... ]])


def R_12(beta):
        return np.array([[ ..., ..., ... ],
                         [ ..., ..., ... ],
                         [ ..., ..., ... ]])


def R_23(gamma):
        return np.array([[ ..., ..., ... ],
                         [ ..., ..., ... ],
                         [ ..., ..., ... ]])

#############################
####### QUESTION 2 ##########
#############################
# write down the 3x1 relative position vectors for link lengths l_i=1
r_3F_in3 = np.array([[...], [...], [...]])
r_23_in2 = np.array([[...], [...], [...]])
r_12_in1 = np.array([[...], [...], [...]])
r_B1_inB = np.array([[...], [...], [...]])


def create_H(R, r):
    # This is a helper function to create the (4,4) homogeneous transform matrix
    # from a (3,3) rotation matrix R and a (3,1) position vector r
    assert R.shape == (3, 3), "Rotation matrix must be size (3,3)"
    assert r.shape == (3, 1), "Relative position vector must be size (3,1)"
    return np.block([[R, r], [0, 0, 0, 1]])


def H_B3(q):
    # Compose the full chain homogeneous transform between the body and 3 frames
    assert q.shape == (3, 1), "Configuration vector q must be size (3,1)"
    alpha, beta, gamma = q[0, 0], q[1, 0], q[2, 0]
    H_B1 = create_H(R_..., r_...)
    H_12 = create_H(..., ...)
    H_23 = create_H(..., ...)
    H_B3 = H_B1 @ ...                  # Hint, the numpy operator for matrix multiply is '@'
    return H_B3


def r_BF_inB(q):
    # Calculate the foot point position vector in body frame for a given
    # configuration q
    assert q.shape == (3, 1), "Configuration vector q must be size (3,1)"
    r = H_... @ np.vstack((r_..., [1]))     # Hint: Must multiply by a 4x1 vector
    return r[:3]

#############################
####### QUESTION 3 ##########
#############################

# Determine the foot point Jacobian J_BF_inB = d(B_r_BF_inB)/dq
def J_BF_inB(q):
    assert q.shape == (3, 1), "Configuration vector q must be size (3,1)"
    alpha, beta, gamma = q[0, 0], q[1, 0], q[2, 0]
    J = np.array([[ ..., ..., ... ],
                         [ ..., ..., ... ],
                         [ ..., ..., ... ]])
    return J

# Check that J is correct for a random configuration using the numerical checker
q_rand = np.random.rand(3, 1)*2*np.pi
Ex1_extras.J_check(J_BF_inB, r_BF_inB, q_rand)

# What generalized velocity dq do you have to apply in a configuration q = [0;60°;-120°]
# to lift the foot in vertical direction with v = [0;0;-1] m/s
dr = np.array([[0], [0], [-1]])
qval = np.pi/180*np.array([[0], [60],  [-120]])

dq = ...   # Hint: np.linalg.pinv() in the function for Moore-Penrose psuedo-inverse
print('Ex 3: Generalised foot velocity dq = {0}.T deg/s'.format(dq.T/np.pi*180))

#############################
####### QUESTION 4 ##########
#############################
# Write an algorithm for the inverse kinematics problem to find the generalized
# coordinates q that gives the end effector position rGoal = [0.2,0.5,-2]'
q0 = np.pi/180*np.atleast_2d([0, -30, 60]).T
r_goal = np.atleast_2d([0.2, 0.5, -2]).T

# enter your algorithm here #
...

print('Ex 4: Inverse kinematics for r = {0}.T: q = {1}.T deg'.format(r_goal.T, q.T/np.pi*180))

#############################
####### QUESTION 5 ##########
#############################
# Write an algorithm for the inverse differential kinematics problem to
# find the generalized velocities dq to follow a circle in the body xz plane
# around the start point rCenter with a radius of r=0.5 and a
# frequency of 1Hz. The start configuration is q =  pi/180*([0,-60,120])'
q0 = np.pi/180*np.atleast_2d([0, -60, 120]).T
dq0 = np.zeros((3,1))
rCenter = r_BF_inB(q0)
radius = 0.5
f = 0.25

rGoal = lambda t: rCenter + radius*np.atleast_2d([np.sin(2*np.pi*f*t),
                                                  0,
                                                  np.cos(2*np.pi*f*t)]).T
drGoal = lambda t: 2*np.pi*f*radius*np.atleast_2d([np.cos(2*np.pi*f*t),
                                                   0,
                                                   -np.sin(2*np.pi*f*t)]).T

# define here the time resolution and controller gain Kp
# Try varying the gain to see the effect!
deltaT = 0.01
timeArr = np.arange(0, 1/f, deltaT)
Kp = 5.0

# q, r, and rGoal are stored for every point in time in the following arrays
qArr = np.zeros((3, len(timeArr)))
rArr = np.zeros((3, len(timeArr)))
rGoalArr = np.zeros((3, len(timeArr)))

q = q0
dq = dq0
for i in range(len(timeArr)):
    t = timeArr[i]

    # data logging, don't change this!
    q = q + deltaT*dq
    qArr[:, [i]] = q
    rArr[:, [i]] = r_BF_inB(q)
    rGoalArr[:, [i]] = rGoal(t)

    # controller:
    # step 1: create a simple p controller to determine the desired foot
    # point velocity
    v = ... + Kp*( ... )
    # step 2: perform inverse differential kinematics to calculate the
    # generalized velocities
    dq = ...

with plt.style.context('ggplot'):
    tp = Ex1_extras.TrajectoryPlotter(timeArr, qArr, rArr, rGoalArr)
    an = tp.animation()
    plt.show()
