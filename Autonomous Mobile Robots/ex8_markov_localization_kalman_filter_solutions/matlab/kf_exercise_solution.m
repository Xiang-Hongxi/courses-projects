%% Autonomous Mobile Robots - Exercise 8 (Kalman Filter)
close all;
clear all;
clc;
global F Q H R motion_model observation_model

%% Experiment parameters
time_duration = 50; % [sec]
dT = 0.5;           % time steps [sec]
g_moon = 1.62;      % m/s2 gravity on the moon
a_thrust = 1.52;    % m/s2 thrust of the rocket engines

R = 10.^2;          % Measurement variance (m^2)
sigma_v = 0.50;     % Standard deviation of velocity noise (iid at each time step)
Q = [dT.^2, dT; dT, 1]*sigma_v.^2;  % Process noise matrix ([dT, 1]'*[dT, 1] * var)

%% (1) SOLUTION
% Motion Model
F = [1.0, dT; 0, 1.0];
B = [0.5 * dT * dT; dT];
motion_model = @(x, u) F * x + B .* u;

% Observation model
H = [1/sin(pi * 0.25), 0];
observation_model = @(x) H * x;

make_observation = @(x) observation_model(x) + sqrt(R) * randn(1);

%% Init
% Time
cur_time = 0.0;
timestamps = cur_time;

% Control input
u = a_thrust - g_moon;

% State at time 0
x_true = [150.0; 0];                    % True state
x_deadreckoning = x_true + [20; -1];    % Initial dead reckoning state
x_estimated = x_deadreckoning;          % Initial estimated state
P = diag([10.^2, 2.^2]);                  % Prior covariance

f1 = figure();
f1.Position(3:4) = [560 720];
ax1 = subplot(4, 1, 1);
title(ax1, 'Height Above Ground')
h_gt = animatedline(ax1, timestamps, x_true(1,1), 'Color','b');
h_dr = animatedline(ax1, timestamps, x_deadreckoning(1,1), 'Color','k');
h_ekf = animatedline(ax1, timestamps, x_estimated(1,1), 'Color','r');
legend(ax1, ["Ground-Truth", "Dead reckoning", "Kalman Filter"]);
ylabel('h (m)');
xlim([0, time_duration]);
%ylim([0, x_true(1,1)*1.2]);

ax2 = subplot(4, 1, 2);
h_vgt = animatedline(ax2, timestamps, x_true(2,1), 'Color','b');
h_vdr = animatedline(ax2, timestamps, x_deadreckoning(2,1), 'Color','k');
h_vekf = animatedline(ax2, timestamps, x_estimated(2,1), 'Color','r');
xlim([0, time_duration]);
%ylim([-10, 2]);
ylabel('dh/dt (m/s)');

ax3 = subplot(4, 1, 3);
h_z = animatedline(ax3, timestamps, make_observation(x_true), 'Color','r', 'Marker','.', 'LineStyle', 'none');
legend(ax3, "Measurements");
xlim([0, time_duration]);
%ylim([0, 1.2*x_true(1,1)*sqrt(2)]);
ylabel('z (m)');

ax4 = subplot(4, 1, 4);
h_var = animatedline(ax4, timestamps, sqrt(P(1,1)), 'Color','m');
legend(ax4, "Height Variance");
xlabel(ax4, "time")
xlim([0, time_duration]);
%ylim([0, 2*sqrt(R)]);
ylabel('\sigma_h (m)');

%% Simulation loop
while cur_time < time_duration
    cur_time = cur_time + dT;

    % Ground-truth trajectory
    x_true = motion_model(x_true, u);   % Normal state update
    v_r = sigma_v*randn(1);             % Sample random disturbance velocity
    x_true = x_true + [dT*v_r; v_r];    % Add to the state
    z = make_observation(x_true);       
    
    if x_true(1,1) <= 0
        break
    end
    
    % Dead reckoning
    x_deadreckoning = motion_model(x_deadreckoning, u);
    
    [x_estimated, P] = kalman_filter(x_estimated, P, u, z);

    % Animation
    
    % Positions
    addpoints(h_gt, cur_time, x_true(1,1));
    addpoints(h_dr, cur_time, x_deadreckoning(1,1));
    addpoints(h_ekf, cur_time, x_estimated(1,1));

    % Velocities
    addpoints(h_vgt, cur_time, x_true(2,1));             
    addpoints(h_vdr, cur_time, x_deadreckoning(2,1));
    addpoints(h_vekf, cur_time, x_estimated(2,1));
    
    addpoints(h_z, cur_time, z);
    
    addpoints(h_var, cur_time, sqrt(P(1,1)));

    pause(0.05)
end
        
%% Implement the kalman filter        
function [x_estimated, P_estimated] = kalman_filter(x, P, u, z)
    % Input variables:
    % @x: Filter State
    % @u: Control Input
    % @z: Measurement
    % @P: 2x2 Covariance matrix
    global F Q H R motion_model observation_model
    
    % Prediction Step
    x_predicted = motion_model(x, u);
    P_predicted = F * P * F' + Q;

    % Update Step if a measurement is available
    z_predicted = observation_model(x_predicted);

    %% SOLUTION
    y = z - z_predicted;
    S = H * P_predicted * H' + R;
    K = P_predicted * H' * inv(S);
    x_estimated = x_predicted + K * y;
    P_estimated = (eye(2) - K * H) * P_predicted;
    
end
