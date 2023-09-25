%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

classdef MPC_TS_SC
    properties
        yalmip_optimizer
    end

    methods
        function obj = MPC_TS_SC(Q,R,N,H,h,S,v,params)            
            % YOUR CODE HERE
            nu = params.model.nu;
            nx = params.model.nx;
            nh = size(params.constraints.StateRHS,1);
            
            U = sdpvar(repmat(nu,1,N),ones(1,N),'full');
            X0 = sdpvar(nx,1,'full');
            X = sdpvar(repmat(nx,1,N+1),ones(1,N+1),'full');
            E = sdpvar(repmat(nh,1,N+1),ones(1,N+1),'full');
            X{1} = X0;

            [~, S_, ~] = dlqr(params.model.A, params.model.B, Q, R);

            objective = 0;
            constraints = [];
            for k = 1:N
                objective = objective + X{k}' * Q * X{k} + U{k}' * R * U{k} + E{k}' * S * E{k} + v * norm(E{k}, Inf);
                constraints = [constraints, X{k+1} == params.model.A * X{k} + params.model.B * U{k}];
                constraints = [constraints, params.constraints.StateMatrix * X{k} <= params.constraints.StateRHS + E{k}];
                constraints = [constraints, params.constraints.InputMatrix * U{k} <= params.constraints.InputRHS];
                constraints = [constraints, E{k} >= zeros(nh,1)];
            end
            constraints = [constraints, H * X{N+1} <= h];
            constraints = [constraints, params.constraints.StateMatrix * X{N+1} <= params.constraints.StateRHS + E{N+1}]; 
            constraints = [constraints, E{N+1} >= zeros(nh,1)];
            objective = objective + X{N+1}' * S_ * X{N+1} + E{N+1}' * S * E{N+1} + v * norm(E{N+1}, Inf);
            
            opts = sdpsettings('verbose',1,'solver','quadprog');
            obj.yalmip_optimizer = optimizer(constraints,objective,opts,X0,{U{1} objective});
        end

        function [u, u_info] = eval(obj,x)
            %% evaluate control action by solving MPC problem, e.g.
            tic;
            [optimizer_out,errorcode] = obj.yalmip_optimizer(x);
            solvetime = toc;
            [u, objective] = optimizer_out{:};

            feasible = true;
            if (errorcode ~= 0)
                feasible = false;
            end

            u_info = struct('ctrl_feas',feasible,'objective',objective,'solvetime',solvetime);
        end
    end
end