%% Autonomous Mobile Robots - Exercise 11 Q2 - Harmonic Potential Fields
close all;
clear all;
clc;

%% 2.1 - Initialisation

% initialize traversability map. 1 for traversable, 0 for obstacle
Map = ones(11,9);
Map(1,:) = 0; Map(11,:) = 0; Map(:,1) = 0; Map(:,9)     = 0;
Map(9,2) = 0; Map(10,2) = 0; Map(10,3)= 0; Map(5:6,5:8) = 0;

% initialize search start and goal locations
SearchStart = [3,7];
SearchGoal  = [9,6];

fh = figure(); fh.Position(3:4) = [800, 400];
ax1 = subplot(1, 2, 1); hold on;
title(ax1, 'Obstacle map');
imshow(Map);
plot(ax1, SearchStart(2), SearchStart(1), 'g^');
plot(ax1, SearchGoal(2), SearchGoal(1), 'ro');

% Initialize iterative search
SearchSolution = zeros(size(Map));
SearchSolution(Map==0)=1;   %set obstacle cells to "1" (high potential)
SearchSolution(Map==1) =0.5; %set free cells to "0.5" (mid potential)
SearchSolution(SearchGoal(1),SearchGoal(2)) = 0;

%% 2.2 Iterative updates
% Iterative parameters (max iterations, convergence tolerance)
tol      = 0.01;
maxIter  = 50;

ax2 = subplot(1, 2, 2); hold on;
title(ax2, 'Potential Field');
hImage = imshow(SearchSolution, 'Colormap', parula);

% Iteratively solve the discrete Laplace Equation with Dirichlet boundary conditions
iter = 0; maxChange = inf;
while maxChange > tol
    iter = iter+1;
    assert(maxIter > iter, 'maxIter assert triggered. Aborting.');

	NextSearchSolution = SearchSolution;
    for x=1:1:size(Map,1)
    	for y=1:1:size(Map,2)
        	if and(Map(x,y)==1, SearchSolution(x,y)~=0)
        		NextSearchSolution(x,y) = 1/4*(SearchSolution(x-1,y) + ...
        	                                   SearchSolution(x+1,y) + ...
        								       SearchSolution(x,y-1) + ...
        		                               SearchSolution(x,y+1) );
        	end
        end
    end
    
    % Convolution solution
    % NextSearchSolution = conv2(SearchSolution, [0, 0.25, 0; 0.25, 0, 0.25; 0, 0.25, 0], 'same');
    % NextSearchSolution(Map==0)=1;
    % NextSearchSolution(SearchGoal(1),SearchGoal(2)) = 0;
        
    maxChange = max(max(abs(SearchSolution-NextSearchSolution)));
    SearchSolution = NextSearchSolution;
    
    % Animate
    pause(0.2);
    set(hImage, 'CData', SearchSolution);
end

hold on;
plot(ax2, SearchStart(2), SearchStart(1), 'g^');
plot(ax2, SearchGoal(2), SearchGoal(1), 'ro');
      
%% 2.3 Backtrack solution
% extract solution path from start to goal
% Construct the path as an n x 2 array, with the start as the first row and
% the goal as the last row. Assume an 8-connected grid

OptimalPath = SearchStart;
iter = 0;
while ~isequal(OptimalPath(end,:),SearchGoal)
    iter = iter+1;
    assert(maxIter > iter, 'maxIter assert triggered. Aborting.');
        
    % extract index corresponding to the minimal
    % value within a 3 by 3 window
    Window = SearchSolution(OptimalPath(end,1)-1:OptimalPath(end,1)+1, ...
                            OptimalPath(end,2)-1:OptimalPath(end,2)+1);
    [x,y] = find(Window==min(min(Window)));
    NextPoint = OptimalPath(end,:)+[x(1)-2,y(1)-2];
    OptimalPath = [OptimalPath; NextPoint];
end
plot(ax2, OptimalPath(:,2), OptimalPath(:,1), 'r-')