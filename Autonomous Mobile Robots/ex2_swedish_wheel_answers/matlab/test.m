Finv=(R'*R)\(R'*J)
thetadot=pi;
% statedot=[0 0 thetadot]';
% statedot=[10 0 0]';
statedot=[];
fai=[];
dt=0.1;
for t=0:dt:10-dt
    newstatedot=[sin(t) -cos(t) 0]';
    statedot=[statedot,newstatedot];
    fai=[fai,Finv*newstatedot];
end

alpha1=0;
alpha2=2/3*pi;
alpha3=4/3*pi;

t=0:dt:10-dt;
subplot(3,1,1)
plot(t,fai(1,:))
subplot(3,1,2)
plot(t,fai(2,:))
subplot(3,1,3)
plot(t,fai(3,:))

plotOmnibot(F, fai, dt);