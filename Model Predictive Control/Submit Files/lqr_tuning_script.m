%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% using function lqr_tuning to perform parameter study
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear;

N = 5;

params = generate_params();

xy_candidate = logspace(-2, 2, N);
z_candidate = [50, 100, 150, 200, 250];

[qx, qy, qvx, qvy] = ndgrid(xy_candidate);
[qz, qvz] = ndgrid(z_candidate);

Q = ones(6,N^4*25);

ref = 1;
for i=1:N
    for j=1:N
        for p=1:N
            for q=1:N
                for v=1:5
                    for z=1:5
                        Q(1,ref) = qx(i,j,p,q);
                        Q(2,ref) = qy(i,j,p,q);
                        Q(3,ref) = qz(v,z);
                        Q(4,ref) = qvx(i,j,p,q);
                        Q(5,ref) = qvy(i,j,p,q);
                        Q(6,ref) = qvz(v,z);
                        ref = ref+1;
                    end
                end
            end
        end
    end
end

x0 = params.model.InitialConditionA;
[tuning_struct, i_opt] = lqr_tuning(x0,Q,params);
q = tuning_struct(i_opt).Qdiag;

% verify the input cost <= 11
if tuning_struct(i_opt).InputCost <= 11
    disp("We have found right q !!")
    save('lqr_tuning_script.mat','tuning_struct','q');
else
    disp("Input cost is too large, retry parameters")
end

% num = 1;
% for n=1:N^4*25
%     if ((tuning_struct(n).TrajFeasible)&&(tuning_struct(n).InputCost<=9))
%         succeed(num) = tuning_struct(n);
%         num =num+1;
%     end
% end