%% Q1
% Write down the rotation matrices as functions of the angles
% alpha, beta, gamma using anonymous functions 
% https://www.mathworks.com/help/matlab/matlab_prog/anonymous-functions.html

R_B1 = @(alpha) [1,0,0;0,cos(alpha),-sin(alpha);0,sin(alpha),cos(alpha)];
R_12 = @(beta)  [cos(beta),0,sin(beta);0,1,0;-sin(beta),0,cos(beta)];
R_23 = @(gamma) [cos(gamma),0,sin(gamma);0,1,0;-sin(gamma),0,cos(gamma)];

%% Q2
% Write down the 3x1 relative position vectors for link lengths l_i=1
r_3F_in3 = [0,0,-1]';
r_23_in2 = [0,0,-1]';
r_12_in1 = [0,0,-1]';
r_B1_inB = [0,1,0]';

% Write down the homogeneous transformations
H_23 = @(gamma) [R_23(gamma),r_23_in2;0 0 0 1];
H_12 = @(beta) [R_12(beta),r_12_in1;0 0 0 1];
H_B1 = @(alpha) [R_B1(alpha),r_B1_inB;0 0 0 1];

% Create the cumulative transformation matrix
% We will assume input of the configuration vector q = [alpha, beta,
% gamma]'
H_B3 = @(q) H_B1(q(1))*H_12(q(2))*H_23(q(3)); 

% find the foot point position vector
H_cut = @(H) H(1:3,:);
r_BF_inB = @(q) (H_cut(H_B3(q))*[r_3F_in3;1]);


%% Q3

% Calculate the foot point Jacobian as a fn of configuration vector 
% q = [alpha; beta; gamma]'
J_BF_inB = @(q)[...
    0, -cos(q(2) + q(3)) - cos(q(2)), -cos(q(2) + q(3));...
    cos(q(1))*(cos(q(2) + q(3)) + cos(q(2)) + 1), -sin(q(1))*(sin(q(2) + q(3)) + sin(q(2))), -sin(q(2) + q(3))*sin(q(1));...
    sin(q(1))*(cos(q(2) + q(3)) + cos(q(2)) + 1),  cos(q(1))*(sin(q(2) + q(3)) + sin(q(2))),  sin(q(2) + q(3))*cos(q(1))];

% what generalized velocity dq do you have to apply in a configuration q = [0;60°;-120°]
% to lift the foot in vertical direction with v = [0;0;-1m/s];
dr = [0;0;-1];
qval = pi/180*([0;60;-120]);

dq = J_BF_inB(qval)\dr;

fprintf('Q3: For target velocity [%0.1f; %0.1f; %0.1f] m/s\n', dr(1), dr(2), dr(3));
fprintf('in current configuration [%0.1f; %0.1f; %0.1f] deg\n', qval(1)*180/pi, qval(2)*180/pi, qval(3)*180/pi);
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
        
% q0 = pi/180*([0,0,0])';
% rGoal = [-1.5, 1.0,-2.5]';

i_max = 100;
r_tolerance = 1e-6;

q = q0;
r = r_BF_inB(q);
r_error = rGoal-r;
i = 1;
while max(abs(r_error)) > r_tolerance
    q = q +  pinv(J_BF_inB(q))*r_error;
    r = r_BF_inB(q);
    r_error = rGoal-r;
    i = i+1;
    if i >= i_max
        fprintf('No solution found within tolerance %d after %d iterations!', r_tolerance, i);
        break;
    end
end
 
qGoal = q;
if max(abs(r_error)) < r_tolerance
    fprintf('Q4: Inverse kinematics for rGoal = [%0.1f; %0.1f; %0.1f]\n', rGoal(1), rGoal(2), rGoal(3));
    fprintf('qGoal = [%0.1f; %0.1f; %0.1f] deg, found in %d iterations\n', qGoal(1)*180/pi, qGoal(2)*180/pi, qGoal(3)*180/pi, i-1);
end


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
    v = drGoal(t)+10.0*(rGoal(t)-r_BF_inB(q));
    % step 2: perform inverse differential kinematics to calculate the
    % gneralized velocities
    dq = J_BF_inB(q)\v;
    
end

plotTrajectory(timeArr, qArr, rArr, rGoalArr, true);

