% Note that there are several possible solutions to this 
% depending on your frame definitions. However, the stacked
% wheel equations should still hold
  
% Wheel 1, the far right wheel
alpha1 = 0.0;
beta1 = 0.0;
ell1 = 0.5;

% Wheel 2, the top left wheel
alpha2 = (2/3)*pi;
beta2 = 0.0;
ell2 = 0.5;
      
% Wheel 3, the bottom left wheel
alpha3 = (4/3)*pi;
beta3 = 0.0;
ell3 = 0.5;

% The wheel radius
r = 0.1;
  
% Build the equations for each wheel by plugging in the parameters
J1 = [sin(alpha1+beta1), -cos(alpha1+beta1), -ell1*cos(beta1)];
J2 = [sin(alpha2+beta2), -cos(alpha2+beta2), -ell2*cos(beta2)];
J3 = [sin(alpha3+beta3), -cos(alpha3+beta3), -ell3*cos(beta3)];  
  
% Stack the wheel equations
J = [J1;J2;J3];
R = r * eye(3);

% Compute the forward differential kinematics matrix, F
F = (J'*J)\J'*R;

%% Try changing the wheel speeds to see what motions the robot does.
numSeconds=10;
dt = 0.1;

% % The speed of the first wheel (rad/s)
% phiDot1 = 1.0*ones(1, numSeconds/dt);
% % The speed of the second wheel (rad/s)
% phiDot2 = 0.5*ones(1, numSeconds/dt);
% % The speed of the third wheel (rad/s)
% phiDot3 = 0.25*ones(1, numSeconds/dt);

% Stationary rotation (1 full rotations in 10 seconds, i.e. 0.1Hz)
% phiDot1 = -2*pi*ell1/(r*numSeconds)*ones(1, numSeconds/dt);
% phiDot2 = phiDot1;
% phiDot3 = phiDot1;

% Linear motion in R_X
% phiDot1 = 0*ones(1, numSeconds/dt);
% phiDot2 = 0.5*ones(1, numSeconds/dt);
% phiDot3 = -phiDot2;

%In a circle (no rotation)
% tt = 0:dt:numSeconds-dt;
% phiDot1 = cos(2*pi*tt/numSeconds);
% phiDot2 = cos(2*pi*tt/numSeconds-alpha2);
% phiDot3 = cos(2*pi*tt/numSeconds-alpha3);

% BONUS: In a circle + constant rotation
tt = 0:dt:numSeconds-dt;
phiDot1 = cos(2*pi*tt/numSeconds) -2*pi*ell1/(r*numSeconds);
phiDot2 = cos(2*pi*tt/numSeconds-alpha2)-2*pi*ell1/(r*numSeconds);
phiDot3 = cos(2*pi*tt/numSeconds-alpha3)-2*pi*ell1/(r*numSeconds);


phiDot = [phiDot1; phiDot2; phiDot3];
  
plotOmnibot(F, phiDot, dt);
