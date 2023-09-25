%% Load test data
clear;
clc;

x = readmatrix('x.csv');
y = readmatrix('y.csv');

draw_points(x, y);

N = size(x, 1); 
assert(N == size(y, 1));

% Compute the centroid of the point set (xmw, ymw) considering that
% the centroid of a finite set of points can be computed as
% the arithmetic mean of each coordinate of the points.
xc = sum(x) / N;
yc = sum(y) / N;

%% Part 1: Derive the parameter alpha

% compute the offset of each point to the centroid
xtilde = xc - x;
ytilde = yc - y;

% compute alpha
num   = -2 * sum(xtilde.*ytilde);
denom = sum(ytilde.^2 - xtilde.^2);
alpha = atan2(num, denom) / 2;

%% Part 2: Derive the parameter r

% compute parameter r by inserting the centroid 
% into the line equation and solve for r
r = xc * cos(alpha) + yc * sin(alpha);

%% Draw the fitted line

hold off;
draw_points(x,y);
hold on;
draw_line(alpha, r);
hold off;

%% Utility functions

function draw_points(x, y)
scatter(x,y);
grid on;
xlabel('x');
ylabel('y');
end

function draw_line(alpha, r)
[xz, yz] = pol2cart(alpha, r);
line_origin = [xz; yz];
delta_vector = [ -sin(alpha); cos(alpha)] * 10;
line_points = [line_origin, line_origin + delta_vector];
line(line_points(1, :), line_points(2, :), 'color', 'r', 'linestyle', '-', 'linewidth', 2);
end