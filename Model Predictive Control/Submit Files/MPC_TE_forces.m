%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2022, Amon Lahr, Simon Muntwiler, Antoine Leeman & Fabian Flürenbrock Institute for Dynamic Systems and Control, ETH Zurich.
%
% All rights reserved.
%
% Please see the LICENSE file that has been included as part of this package.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

classdef MPC_TE_forces
    properties
        forces_optimizer
    end

    methods
        function obj = MPC_TE_forces(Q,R,N,params)
            % YOUR CODE HERE
            nu = params.model.nu;
            nx = params.model.nx;
            
            U = sdpvar(repmat(nu,1,N),ones(1,N),'full');
            X0 = sdpvar(nx,1,'full');
            X = sdpvar(repmat(nx,1,N+1),ones(1,N+1),'full');
            X{1} = X0;

            objective = 0;
            constraints = [];
            for k = 1:N
                objective = objective + X{k}' * Q * X{k} + U{k}' * R * U{k};
                constraints = [constraints, X{k+1} == params.model.A * X{k} + params.model.B * U{k}];
                constraints = [constraints, params.constraints.StateMatrix * X{k} <= params.constraints.StateRHS];
                constraints = [constraints, params.constraints.InputMatrix * U{k} <= params.constraints.InputRHS];
            end
            constraints = [constraints, X{N+1} == 0];
            constraints = [constraints, params.constraints.StateMatrix * X{N+1} <= params.constraints.StateRHS];

            opts = getOptions('forcesSolver');
            opts.printlevel = 0;
            obj.forces_optimizer = optimizerFORCES(constraints,objective,opts,X0,U{1},{'initial_state'},{'first_control_input'});% YOUR CODE HERE
        end

        function [u, u_info] = eval(obj,x)
            %% evaluate control action by solving MPC problem, e.g.
            [optimizer_out,errorcode,info] = obj.forces_optimizer(x);
            u = optimizer_out;
            objective = info.pobj;
            solvetime = info.solvetime;

            feasible = true;
            if any(errorcode ~= 1)
                feasible = false;
                warning('MPC infeasible');
            end

            u_info = struct('ctrl_feas',feasible,'objective',objective,'solvetime',solvetime);
        end
    end
end