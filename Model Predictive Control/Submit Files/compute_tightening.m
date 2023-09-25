%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function params_z_tube = compute_tightening(K_tube,H_tube,h_tube,params_z)  
	% YOUR CODE HERE

    % initialize params_z
    params_z_tube = params_z;

    Hx = params_z.constraints.StateMatrix;
    hx = params_z.constraints.StateRHS;
    Hu = params_z.constraints.InputMatrix;
    hu = params_z.constraints.InputRHS;
    
    Xz = Polyhedron(Hx,hx);
    Uz = Polyhedron(Hu,hu);

    epsilon = Polyhedron(H_tube,h_tube);

    Xz_tight = Xz - epsilon;
    Uz_tight = Uz - K_tube*epsilon;

    Xz_tight.minHRep();
    Uz_tight.minHRep();
    
    params_z_tube.constraints.StateMatrix = Xz_tight.A;
    params_z_tube.constraints.StateRHS = Xz_tight.b;

    params_z_tube.constraints.InputMatrix = Uz_tight.A;
    params_z_tube.constraints.InputRHS = Uz_tight.b;


end