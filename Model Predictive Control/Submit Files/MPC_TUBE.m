%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

classdef MPC_TUBE
    properties
        yalmip_optimizer
        K_tube
    end

    methods
        function obj = MPC_TUBE(Q,R,N,H_N,h_N,H_tube,h_tube,K_tube,params_z_tube)
            obj.K_tube = K_tube;

            % YOUR CODE HERE
            nu = params_z_tube.model.nu;
            nx = params_z_tube.model.nx;
            
            V = sdpvar(repmat(nu,1,N),ones(1,N),'full');
            X0 = sdpvar(nx,1,'full');
            Z = sdpvar(repmat(nx,1,N+1),ones(1,N+1),'full');
          
            [~, S, ~] = dlqr(params_z_tube.model.A, params_z_tube.model.B, Q, R);

            objective = 0;

            constraints = [H_tube * (X0-Z{1}) <= h_tube];

            for k = 1:N
                objective = objective + Z{k}' * Q * Z{k} + V{k}' * R * V{k};
                constraints = [constraints, Z{k+1} == params_z_tube.model.A * Z{k} + params_z_tube.model.B * V{k}];
                constraints = [constraints, params_z_tube.constraints.StateMatrix * Z{k} <= params_z_tube.constraints.StateRHS];
                constraints = [constraints, params_z_tube.constraints.InputMatrix * V{k} <= params_z_tube.constraints.InputRHS];
            end
            constraints = [constraints, H_N * Z{N+1} <= h_N];
            constraints = [constraints, params_z_tube.constraints.StateMatrix * Z{N+1} <= params_z_tube.constraints.StateRHS]; 
            objective = objective + Z{N+1}' * S * Z{N+1};
            

            opts = sdpsettings('verbose',1,'solver','quadprog');
            obj.yalmip_optimizer = optimizer(constraints,objective,opts,X0,{V{1} Z{1} objective});
        end

        function [u, u_info] = eval(obj,x)
            %% evaluate control action by solving MPC problem, e.g.
            tic;
            [optimizer_out,errorcode] = obj.yalmip_optimizer(x);
            solvetime = toc;
            % YOUR CODE HERE
            [v, z, objective] = optimizer_out{:};
            u = v + obj.K_tube*(x-z);
            
            feasible = true;
            if (errorcode ~= 0)
                feasible = false;
            end

            u_info = struct('ctrl_feas',feasible,'objective',objective,'solvetime',solvetime);
        end
    end
end