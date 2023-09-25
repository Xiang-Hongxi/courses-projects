%% Autonomous Mobile Robots - Exercise 11 Q2 - Harmonic Potential Fields
close all;
clear all;
clc;

% NOTE: You will need to add code at all places with '...'

%% 2.1 - Initialisation

% initialize traversability map. 1 for traversable, 0 for obstacle
Map = ...;

% initialize search start and goal locations
SearchStart = ...;
SearchGoal  = ...;

fh = figure(); fh.Position(3:4) = [800, 400];
ax1 = subplot(1, 2, 1); hold on;
title(ax1, 'Obstacle map');
imshow(Map);
plot(ax1, SearchStart(2), SearchStart(1), 'g^');
plot(ax1, SearchGoal(2), SearchGoal(1), 'ro');

% Initialize iterative search
% Set obstacle cells to high potential, goal to low potential
SearchSolution = ...;

%% 2.2 Iterative updates

% Iterative parameters (max iterations, convergence tolerance)
tol      = 0.01;
maxIter  = 50;

% Plotting
ax2 = subplot(1, 2, 2); hold on;
title(ax2, 'Potential Field');
hImage = imshow(SearchSolution, 'Colormap', parula);

% Iteratively solve the discrete Laplace Equation with Dirichlet boundary conditions
iter = 0; maxChange = inf;
while maxChange > tol
    iter = iter+1;
    assert(maxIter > iter, 'maxIter assert triggered. Aborting.');

	% ADD YOUR SOLVER LOOP HERE
    % You can overwrite potential_field during each loop, but be careful!
    % The update rule is a function of the old potential values, so if you 
    % update in-place, you could encounter issues!
    ...
    
    % Animate
    pause(0.2);
    set(hImage, 'CData', SearchSolution);
end

hold on;
plot(ax2, SearchStart(2), SearchStart(1), 'g^');
plot(ax2, SearchGoal(2), SearchGoal(1), 'ro');
      
%% 2.3 Backtrack solution
% Extract solution path from start to goal
% Construct the path as an n x 2 array, with the start as the first row and
% the goal as the last row. Assume an 8-connected grid.

OptimalPath = SearchStart;
iter = 0;
while ~isequal(OptimalPath(end,:),SearchGoal)
    iter = iter+1;
    assert(maxIter > iter, 'maxIter assert triggered. Aborting.');
        
    % extract index corresponding to the minimal
    % value within a 3 by 3 window
    
    NextPoint = ...
    OptimalPath = [OptimalPath; NextPoint];
end
plot(ax2, OptimalPath(:,2), OptimalPath(:,1), 'r-')