% Note that there are several possible solutions to this 
% depending on your frame definitions. However, the stacked
% wheel equations should still hold


% Wheel 1, the far right wheel
alpha1 = ...
beta1 = ...
ell1 = ...

% Wheel 2, the top left wheel
alpha2 = ...
beta2 = ...
ell2 = ...
      
% Wheel 3, the bottom left wheel
alpha3 = ...
beta3 = ...
ell3 = ...

% The wheel radius
r = 0.1;
  
% Build the equations for each wheel by plugging in the parameters
J1 = ...
J2 = ...
J3 = ...
  
% Stack the wheel equations
J = [J1;J2;J3];
R = ...

% Compute the forward differential kinematics matrix, F
F = ...

%% Try changing the wheel speeds to see what motions the robot does.
numSeconds=10;
dt = 0.1;

% The speed of the first wheel (rad/s)
phiDot1 = 1.0*ones(1, numSeconds/dt);
% The speed of the second wheel (rad/s)
phiDot2 = 0.5*ones(1, numSeconds/dt);
% The speed of the third wheel (rad/s)
phiDot3 = 0.25*ones(1, numSeconds/dt);

phiDot = [phiDot1; phiDot2; phiDot3];
  
plotOmnibot(F, phiDot, dt);
