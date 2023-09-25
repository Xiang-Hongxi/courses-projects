%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% BRIEF:
%   Template for explicit invariant set computation. You MUST NOT change
%   the output.
% INPUT:
%   Q, R: State and input weighting matrix
% OUTPUT:
%   H, h: Describes polytopic X_LQR = {x | H * x <= h}

function [H, h] = lqr_maxPI(Q,R,params)
	% YOUR CODE HERE
    ctrl = LQR(Q,R,params);
    F_inf = ctrl.K;
    A = [params.constraints.StateMatrix; params.constraints.InputMatrix*F_inf];
    b = [params.constraints.StateRHS; params.constraints.InputRHS];
    system = LTISystem('A', params.model.A+params.model.B*F_inf);
    domain = Polyhedron('A',A,'b',b);
    system.setDomain('x',domain);
    InvSet = system.invariantSet();
    H = InvSet.A;
    h = InvSet.b;
end

