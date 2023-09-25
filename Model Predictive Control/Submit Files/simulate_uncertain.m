%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [Xt,Ut,u_info] = simulate_uncertain(x0, ctrl, Wt, params_z)
	% YOUR CODE HERE
    Nt = params_z.model.HorizonLength;
    Xt = x0;
    Ut = [];
    
    for i=1:Nt
        [u, info] = ctrl.eval(Xt(:,i));        
        Ut = [Ut, u];
        u_info(i) = info;
        x = params_z.model.A*Xt(:,i) + params_z.model.B*u + Wt(:,i);
        Xt = [Xt, x];
    end
end