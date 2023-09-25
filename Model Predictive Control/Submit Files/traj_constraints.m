%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [s_max, y_max, u_max, J_u, df_max, vf_max, traj_feas] = traj_constraints(x,u,params)
    % YOUR CODE HERE
    num_tra = size(x,3);
    num_step = size(x,2);

    for i=1:num_tra
        s_max(i) = 0;
        y_max(i) = 0;
        u_max(i) = 0;
        J_u(i) = 0;
        df_max(i) = 0;
        vf_max(i) = 0;

        s1 = max(abs(x(1,:,i)));
        s2 = max(abs(x(3,:,i)));
        s_max(i) = max(s1, s2);

        y_max(i) = max(abs(x(2,:,i)));
        
        df_max(i) = sqrt(x(1,num_step,i)^2+x(2,num_step,i)^2+x(3,num_step,i)^2);
        vf_max(i) = sqrt(x(4,num_step,i)^2+x(5,num_step,i)^2+x(6,num_step,i)^2);

        u_max(i) = max(max(abs(u(:,:,i))));

        for p=1:(num_step-1)
            J_u(i) = J_u(i) + dot(u(:,p,i),u(:,p,i));
        end

        traj_feas(i) = false;
        if((s_max(i)<=params.constraints.MaxAbsPositionXZ)&&(y_max(i)<=params.constraints.MaxAbsPositionY)...
            &&(u_max(i)<=params.constraints.MaxAbsThrust)&&(df_max(i)<=params.constraints.MaxFinalPosDiff)...
            &&(vf_max(i)<=params.constraints.MaxFinalVelDiff))
            traj_feas(i) = true;
        end
    end
end

