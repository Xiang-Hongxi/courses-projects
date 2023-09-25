%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [Xt,Ut,u_info] = simulate(x0, ctrl, params)

    % YOUR CODE HERE
    Nt = params.model.HorizonLength;
    Xt = x0;
    
    for i=1:Nt
        [u, info] = ctrl.eval(Xt(:,i));
        if i==1
            Ut = u;
        else
            Ut = [Ut, u];
        end
        u_info(i) = info;
        x = params.model.A*Xt(:,i)+params.model.B*u;
        Xt = [Xt, x];
    end
    % Hint: you can access the control command with ctrl.eval(x(:,i))

end