clear;
clc;
for ixh=1:8
app=num2str(ixh);  
AA=[];
mstruct=defaultm('mercator');
mstruct.geoid=[ 6378137,0.0818191908426215];
mstruct.origin=[0,0,0];
mstruct=defaultm(mstruct);
datasetname = ['D:\Matlab\2017\Sturnus_vulgaris\result_',app,'.xls'];
xx=xlsread(datasetname,'Sheet1');
X=xx(:,1);
Y=xx(:,2);
N = size(X,1);


for i1=1:N %200000m*200000m as a cell
yzuobiao=ceil((Y(i1)-10799.5404530279)/200000);% 36 
xzuobiao=ceil((X(i1)+14796209.33)/200000); %35 
AA(i1,3)=xzuobiao; %
AA(i1,4)=yzuobiao;
AA(i1,5)=xzuobiao+35*(yzuobiao-1); 
end
i3=1;
BB=AA(:,5);
for i2=1:N-1 
CC(1)=BB(1);
if BB(i2+1,:) ~= BB(i2,:)
CC(i3+1,:)=BB(i2+1,:);
i3=i3+1;
end
end

N = size(CC,1);
for i4=N+1:364
CC(i4,:)=0;
end 
AA(:,6)=CC;

datasetname_1 = [app,'.xls'];
            
datasetsize1 = ['A1:A',num2str(N)];
datasetsize2 = ['B1:B',num2str(N)];
datasetsize3 = ['C1:C',num2str(N)];
datasetsize4 = ['D1:D',num2str(N)];
datasetsize5 = ['E1:E',num2str(N)];
datasetsize6 = ['F1:F',num2str(N)];

xlswrite(datasetname_1,AA(:,1),datasetsize1);
xlswrite(datasetname_1,AA(:,2),datasetsize2);
xlswrite(datasetname_1,AA(:,3),datasetsize3);
xlswrite(datasetname_1,AA(:,4),datasetsize4);
xlswrite(datasetname_1,AA(:,5),datasetsize5);
xlswrite(datasetname_1,AA(:,6),datasetsize6);
end
