%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [A, B] = generate_system(Ac, Bc, params)
    % YOUR CODE HERE
    deltaT = params.model.TimeStep;
    nx = params.model.nx;
    nu = params.model.nu;

    Cc = eye(nx);
    Dc = zeros(nx,nu);
    sys_cont = ss(Ac, Bc, Cc, Dc);
    sysd = c2d(sys_cont, deltaT); % default'zoh'
    A = sysd.A;
    B = sysd.B;
end