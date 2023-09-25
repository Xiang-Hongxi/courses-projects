
clear,clc

%% initialize parameters

q_star = [91.5;0.0924;248;0;0;0];
Q_star = diag(q_star);

params = generate_params();
R_star = eye(params.model.nu);

N = 30;

% X0 = params.model.InitialConditionA; 
X0 = params.model.InitialConditionB;
% X0 = params.model.InitialConditionC;

[H, h] = lqr_maxPI(Q_star,R_star,params);

%% solve original MPC problem

mpcts = MPC_TS(Q_star,R_star,N,H,h,params);

[Xt1,Ut1,u_info1] = simulate(X0, mpcts, params); %simulate

%% solve soft constraints MPC problem

%choice of S and v
S= eye(size(params.constraints.StateRHS,1)); %dim
v= 1000;
mpctssc = MPC_TS_SC(Q_star,R_star,N,H,h,S,v,params);

[Xt2,Ut2,u_info2] = simulate(X0, mpctssc, params); %simulate

%% verify the control inputs are same

%tolerance
tor = 1e-4;

for i = 1:size(Ut1,2)
    difference_at_time_i(i) = norm((Ut1(:,i)- Ut2(:,i)),inf);
end

maxdifference = max(difference_at_time_i); %()

if maxdifference <= tor
    disp("Control inputs are indeed same!!")
    save('MPC_TS_SC_params.mat','S','v');
else
    disp("Control inputs are not same, retry S and v !!")
end