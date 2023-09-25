clear,clc

%% initialize parameters
qz_star = 248;
qvz_star = 0;
q = [qz_star, qvz_star];
Q = diag(q);

R = 1;
N = 50;

p = [0.1 0.5];

%% design controller
[params] = generate_params();
[params_z] = generate_params_z(params);
K_tube = compute_tube_controller(p,params_z);

[H_tube,h_tube,~] = compute_minRPI(K_tube,params_z);
epsilon = Polyhedron(H_tube,h_tube);
epsilon.minHRep();

params_z_tube = compute_tightening(K_tube,H_tube,h_tube,params_z);

[H_N, h_N] = lqr_maxPI(Q,R,params_z_tube);

save('MPC_TUBE_params.mat','p','K_tube','H_tube','h_tube',"H_N","h_N",'params_z_tube');

%% set up MPC
TUBEMPCController = MPC_TUBE(Q,R,N,H_N,h_N,H_tube,h_tube,K_tube,params_z_tube);