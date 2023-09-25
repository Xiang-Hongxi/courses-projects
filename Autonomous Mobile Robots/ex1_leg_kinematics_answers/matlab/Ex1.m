%% Q1
% Write down the rotation matrices as functions of the angles
% alpha, beta, gamma using anonymous functions 
% https://www.mathworks.com/help/matlab/matlab_prog/anonymous-functions.html
% Hint: R_B1 = @(alpha) [1,0,0; 0, cos(alpha), -sin(alpha); ... ];

R_B1 = @(alpha) ... ;
R_12 = @(beta)  ... ;
R_23 = @(gamma) ... ;



%% Q2
% Write down the 3x1 relative position vectors for link lengths l_i=1
r_3F_in3 = ...;
r_23_in2 = ...;
r_12_in1 = ...;
r_B1_inB = ...;

% Write down the homogeneous transformations
% Hint: Can be created as compound matrices: [R_XY(gamma), r_XY_inX; 0 0 0 1];
H_23 = @(gamma) ...;
H_12 = @(beta) ...;
H_B1 = @(alpha) ...;

% Create the cumulative transformation matrix
% We will assume input of the configuration vector q = [alpha, beta,
% gamma]'
% Hint: H_B3 is a product of the matrices above
H_B3 = @(q) ...; 

% find the foot point position vector
% Hint: This H_cut function just cuts out the first three rows of an H
% matrix to help recover a 3*1 vector. 
% Then, r_XY_inX = @(q) H_cut(H_XZ(q))*[r_ZY_inZ; 1];
H_cut = @(H) H(1:3,:);
r_BF_inB = @(q) ...;


%% Q3

% Calculate the foot point Jacobian as a fn of configuration vector 
% q = [alpha; beta; gamma]'
J_BF_inB = @(q) [...];
    
% what generalized velocity dq do you have to apply in a configuration q = [0;60°;-120°]
% to lift the foot in vertical direction with v = [0;0;-1m/s];
dr = [0; 0; -1];
qval = pi/180*([0; 60; -120]);

dq = ...;

fprintf('Q3: Target velocity r_dot = [%0.1f; %0.1f; %0.1f] m/s\n', dr(1), dr(2), dr(3));
fprintf('in current configuration q = [%0.1f; %0.1f; %0.1f] deg\n', qval(1)*180/pi, qval(2)*180/pi, qval(3)*180/pi);
fprintf('Requires qdot = [%0.1f; %0.1f; %0.1f] deg/s\n', dq(1)*180/pi, dq(2)*180/pi, dq(3)*180/pi);
fprintf('\n\n');


%% Q4

% write an algorithm for the inverse kinematics problem to
% find the generalized coordinates q that gives the end effector position 
% rGoal = [0.2,0.5,-2]' and store it in qGoal
q0 = pi/180*([0;-30;60]);
rGoal = [0.2;0.5;-2];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% enter here your algorithm
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
...
 



%% Q5

% Write an algorithm for the inverse differential kinematics problem to
% find the generalized velocities dq to follow a circle in the body xz plane
% around the start point rCenter with a radius of r=0.5 and a 
% frequeny of 1Hz. The start configuration is q =  pi/180*([0,-60,120])'
q0 = pi/180*([0,-60,120])';
dq0 = zeros(3,1);
rCenter = r_BF_inB(q0);
radius = 0.5;
f = 0.25;
rGoal = @(t) rCenter + radius*[sin(2*pi*f*t),0,cos(2*pi*f*t)]';
drGoal = @(t) 2*pi*f*radius*[cos(2*pi*f*t),0,-sin(2*pi*f*t)]';

% define here the time resolution
deltaT = 0.01;
timeArr = 0:deltaT:1/f;

% q, r, and rGoal are stored for every point in time in the following arrays
qArr = zeros(3,length(timeArr));
rArr = zeros(3,length(timeArr));
rGoalArr = zeros(3,length(timeArr));

q = q0;
dq = dq0;
for i=1:length(timeArr)
    t = timeArr(i);
    % data logging, don't change this!
    q = q+deltaT*dq;
    qArr(:,i) = q;
    rArr(:,i) = r_BF_inB(q);
    rGoalArr(:,i) = rGoal(t);
    
    % controller: 
    % step 1: create a simple p controller to determine the desired foot
    % point velocity
    v = ...
    % step 2: perform inverse differential kinematics to calculate the
    % gneralized velocities
    dq = ...
    
end

plotTrajectory(timeArr, qArr, rArr, rGoalArr, true);

