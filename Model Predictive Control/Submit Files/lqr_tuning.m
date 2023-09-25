%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [tuning_struct, i_opt] = lqr_tuning(x0,Q,params)
    % YOUR CODE HERE
    M = size(Q,2);
    R = eye(params.model.nu);

    for i=1:M
        controller = LQR(diag(Q(:,i)), R, params);
        [Xt, Ut, ~] = simulate(x0, controller, params);
        x(:,:,i) = Xt;
        u(:,:,i) = Ut;
    end

    [s_max, y_max, u_max, J_u, df_max, vf_max, traj_feas] = traj_constraints(x,u,params);
    for j=1:M
        tuning_struct(j).InitialCondition = x0;
        tuning_struct(j).Qdiag = Q(:,j);
        tuning_struct(j).MaxAbsPositionXZ = s_max(j);
        tuning_struct(j).MaxAbsPositionY = y_max(j);
        tuning_struct(j).MaxAbsThrust = u_max(j);
        tuning_struct(j).InputCost = J_u(j);
        tuning_struct(j).MaxFinalPosDiff = df_max(j);
        tuning_struct(j).MaxFinalVelDiff = vf_max(j);
        tuning_struct(j).TrajFeasible = traj_feas(j);
    end
    tuning_struct = transpose(tuning_struct);

    flag = 0;
    for m=1:M
        if tuning_struct(m).TrajFeasible
            flag = flag+1;
            candidate(flag) = tuning_struct(m).InputCost;
            index(flag) = m;
        end
    end
    if flag==0
        i_opt = nan;
    else
        [~,ref] = min(candidate);
        i_opt = index(ref);
    end
end