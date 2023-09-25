%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [H_tube,h_tube,n_iter] = compute_minRPI(K_tube,params_z)
    % YOUR CODE HERE
%     w_max = params_z.constraints.MaxAbsDisturbance;
%     W = Polyhedron([w_max w_max;w_max -w_max;-w_max w_max;-w_max -w_max]);
    AK = params_z.model.A + params_z.model.B*K_tube; 
    H_w = params_z.constraints.DisturbanceMatrix;  
    h_w = params_z.constraints.DisturbanceRHS;
    W = Polyhedron(H_w,h_w);
    W.minHRep()

    n_iter = 0;
    epsilon(n_iter+1) = Polyhedron([0 0]); %initialize epsilon

    while true
        epsilon(n_iter+2) = epsilon(n_iter+1) + AK^n_iter*W;

        epsilon(n_iter+1).minHRep();
        epsilon(n_iter+2).minHRep();

        if eq(epsilon(n_iter+2),epsilon(n_iter+1))  
            break
        else
            n_iter = n_iter + 1;
        end     
    end

     epsilon(n_iter).minHRep();
     H_tube = epsilon(n_iter).A;
     h_tube = epsilon(n_iter).b;

end