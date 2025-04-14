%%
clear;
close all;
clc;

%%
disp('ATTENTION to the slow_data file: this code assumes that:' )
disp('Temperature data n.1 (manual sensor) are in column 3: T1 = dataTrh{3};') 
disp('Relative Humidity data n.1 (manual sensor)are in column 4: RH1 =dataTrh{4}'); 
disp('Temperature data n.2 (FIXED sensor)are in column 5: Tfix = dataTrh{5};') 
disp('Relative Humidity data n.2 (FIXED sensor)are in column 6: RHfix =dataTrh{6}'); 
disp('Pressure data are in column 5: P = dataTrh{7};')
disp('OTHERWISE CHANGE THE ORDER OF columns in this code')
disp('***********************************************')


tic;
%%
%cd('C:\Users\LSL\Documents\UNIBO\Didattica\');  % type in working directory

filenameSonic='TOA5_6550_sonic_data_7.dat'; %type in the name of the file containing the sonic data  
filenameHygrometer='TOA5_6550_slow_data_7.dat';  %type in the name of the file containing the thermohygrometer data  

mn = input('Define the averaging window in seconds: ');

if mn<1
    disp('Error! Please insert a number >=1');
    mn = input('Define the averaging window in seconds: ');
end
%% ------------- SONIC DATA (u,v,w,Ts)---------------------------------

%% Open and scan the Sonic .dat file (comma separated)
fid = fopen(filenameSonic,'rt');    

dataSonic = textscan(fid,'%s %f %f %f %f %f','Delimiter',',','HeaderLines',4);
fclose(fid);


fid = fopen(filenameSonic,'rt');    

dataSonic = textscan(fid,'%s %f %f %f %f %f','Delimiter',',','HeaderLines',4);
fclose(fid);

%% Sonic Data 
%timeS=data{1}; %--->date & time string
%RN=data{2}; %--->Record number
u = dataSonic{3};   %-----> u-component of wind velocity (anemometer reference system --> positive toward north)
v = dataSonic{4};   %-----> v-component of wind velocity (anemometer reference system --> positive toward west)
w = dataSonic{5};   %-----> w-component of wind velocity (anemometer reference system --> positive upward)
Ts = dataSonic{6};  %-----> Ts sonic temperature

%% Exclude uncompleted minutes at the beginning and at the end of the Sonic Datafile

Datetime_Sonic = datenum(dataSonic{1});% Convert date and time to serial date number (Matlab time format)
% Starting time
t1=datevec(dataSonic{1}(1));
timeStart=datenum([t1(1:4),t1(5)+1,0]);%next minute
[b1,~]=find(Datetime_Sonic<timeStart);

%End time
t2=datevec(dataSonic{1,1}(end));
timeEnd=datenum([t2(1:4),t2(5),0]);
[b2,~]=find(Datetime_Sonic>=timeEnd);

%exclude uncompleted minutes at the beginning and the end of the file
Datetime_Sonic([b1;b2])=[];
u([b1;b2])=[];
v([b1;b2])=[];
w([b1;b2])=[];
Ts([b1;b2])=[];
%Display
disp(['Dataset begins at  = ' char(datetime(datevec(Datetime_Sonic(1))))]);
disp(['Dataset ends at  = ' char(datetime(datevec(Datetime_Sonic(end))))]);


%% Definition of the averaging window
npos = length(u);            % data matrix dimension
samp_freq = 20;                      % sample frequency
n_int = npos/(mn*samp_freq);         % Number of intervals for the average windows 
nA_avg = npos/n_int;                 % Elements of an averaging windows
nA_avg = floor(nA_avg); % make nA_avg an integer number
nA_x = 1:nA_avg;


%% Averaging
b=1;
for bb=0:nA_avg:npos-nA_avg
    uavg(b,1) = mean(u(bb+nA_x));        %  mean of u-component over the selected averaging window
    vavg(b,1) = mean(v(bb+nA_x));        %  mean of v-component over the selected averaging window
    wavg(b,1) = mean(w(bb+nA_x));        %  mean of w-component over the selected averaging window
    Tsavg(b,1) = mean(Ts(bb+nA_x));      %  mean of sonic temperature over the selected averaging window
    
    %calculate  variance 
    u_var_series(b,1)=var(u(bb+nA_x));
    v_var_series(b,1)=var(v(bb+nA_x));
    w_var_series(b,1)=var(w(bb+nA_x));
    Ts_var_series(b,1)=var(Ts(bb+nA_x));
    
    Datetime_Sonic_avg(b,1)=Datetime_Sonic(bb+nA_x(end));
    
    b=b+1;
    
end

%% Save Sonic averaged data to file

time_Sonic=[1:1:length(uavg)]'.*mn; %time of the averaged data. It is expressed in consecutive seconds from the first data point

output_avg = [time_Sonic uavg vavg wavg Tsavg];
save(['' num2str(mn) '_sec_avg_Sonic.dat'],'output_avg','-ascii','-tabs');  % averaged data are saved in the same folder 

%save in excel format
T1= table(time_Sonic,uavg, vavg, wavg, Tsavg);
writetable(T1,['' num2str(mn) '_sec_avg_Sonic.xlsx']);

%% Total Variance
var_u = var(u);
var_v = var(v);
var_w = var(w);
var_Ts = var(Ts);
disp(['Var(u) = ' num2str(var_u) '']);
disp(['Var(v) = ' num2str(var_v) '']);
disp(['Var(w) = ' num2str(var_w) '']);
disp(['Var(Ts) = ' num2str(var_Ts) '']);

%% Plot Sonic timeseries

figure(1)
plot(Datetime_Sonic_avg,uavg,Datetime_Sonic_avg,vavg,Datetime_Sonic_avg,wavg);
datetick('x','HH:MM');
legend('u','v','w','FontSize',12);
ylabel('Velocity Components [ms^-^1]');
xlabel('time')
ax = gca; % current axes
ax.FontSize = 12;

figure(2)
plot(Datetime_Sonic_avg,Tsavg);
datetick('x','HH:MM');
ylabel(['Ts (' char(176) 'C)'])
xlabel('time')
ax = gca; % current axes
ax.FontSize = 12;
title(['Time Average=', num2str(mn),'s']);

figure(3)
plot(Datetime_Sonic_avg,u_var_series,Datetime_Sonic_avg,v_var_series,Datetime_Sonic_avg,w_var_series);
datetick('x','HH:MM');
legend('Var(u)','Var(v)','Var(w)','FontSize',12);
xlabel('time')
ylabel('Velocity Variance [m^2s^-^2]')
ax = gca; % current axes
ax.FontSize = 12;
title(['Time Average=', num2str(mn),'s']);

figure(4)
plot(Datetime_Sonic_avg,Ts_var_series);
datetick('x','HH:MM');
xlabel('time')
ylabel(['Ts Variance [' char(176) 'C^2]'])
ax = gca; % current axes
ax.FontSize = 12;
title(['Time Average=', num2str(mn),'s']);
%% Probability Density Function

%Show PDF of u,v,w
pd_u = dfittool(uavg,[],[],'u');      % Gaussian distribution of u
pd_v = dfittool(vavg,[],[],'v');      % Gaussian distribution of u
pd_w = dfittool(wavg,[],[],'w');      % Gaussian distribution of u

%% Scatter plot w vs T
figure(5)

plot(Tsavg,wavg,'.r','MarkerSize',13);
ylabel('w (m/s)')
xlabel(['Ts [' char(176) 'C]'])
ax = gca; % current axes
ax.FontSize = 12;
title(['Time Average=', num2str(mn),'s']);

%% --------------SLOW DATA (T/RH)-----------------------------------------

%% Open and scan the Slow .dat file (comma separated)
fid = fopen(filenameHygrometer,'rt');    
dataTrh = textscan(fid,'%s %f %f %f %f %f %f','Delimiter',',','HeaderLines',4);
fclose(fid);
%% T,RH,P data
%timeTrh=dataTrh{1}; %--->date & time string
%RN=dataTrh{2}; %--->Record number
T1 = dataTrh{3};   %-----> air temperatur in Celsius
RH1 =dataTrh{4};   %-----> Relative humidity in %
Tfix = dataTrh{5};   %-----> air temperatur in Celsius
RHfix =dataTrh{6};   %-----> Relative humidity in %
P = dataTrh{7};   %-----> Atmospheric Pressure in hPa

%% Exclude uncompleted minutes at the beginning and at the end of the Slow Datafile 
Datetime_Trh=datenum(datevec(dataTrh{1}));% Convert date and time to serial date number (Matlab time format)
% Starting time
[b3,~]=find(Datetime_Trh<timeStart);
%End time
[b4,~]=find(Datetime_Trh>=timeEnd);

%exclude uncompleted minutes at the beginning and the end of the file
Datetime_Trh([b3;b4])=[];
T1([b3;b4])=[];
RH1([b3;b4])=[];
Tfix([b3;b4])=[];
RHfix([b3;b4])=[];
P([b3;b4])=[];

% %Display
% disp(['Dataset begins at  = ' char(datetime(datevec(Datetime_Trh(1))))]);
% disp(['Dataset ends at  = ' char(datetime(datevec(Datetime_Trh(end))))]);
%% Average and Save of thermohygrometer and Barometer data 
if mn>1 %if time interval (mn) is greater than 1, then make the average
    npos2 = length(T1);           % data matrix dimension
    samp_freq2 = 1;                         % sample frequency
    n_int2 = npos2/(mn*samp_freq2);         % Number of intervals for the average windows
    nA_avg2 = npos2/n_int2;                 % Elements of an averaging windows
    nA_avg2 = floor(nA_avg2); % make nA_avg an integer number
    nA_x2 = 1:nA_avg2;
    
    %Averaging
    bt=1;
    for bb2=0:nA_avg2:npos2-nA_avg2
        Tavg1(bt,1) = mean(T1(bb2+nA_x2));
        RHavg1(bt,1) = mean(RH1(bb2+nA_x2)); 
        TavgFix(bt,1) = mean(Tfix(bb2+nA_x2));
        RHavgFix(bt,1) = mean(RHfix(bb2+nA_x2)); 
        Pavg(bt,1) = mean(P(bb2+nA_x2)); 
        Datetime_Trh_avg(bt,1)=Datetime_Trh(bb2+nA_x2(end));
               
        bt=bt+1;
    end
    
  
    
% Save averaged data to .dat and .xlsx file
    
    time_Trhavg=[1:1:length(Tavg1)]'.*mn; %time of the averaged data. It is expressed in consecutive seconds from the first data point
    
    output_avg2 = [time_Trhavg Tavg1 RHavg1 TavgFix RHavgFix Pavg];
    save(['' num2str(mn) '_sec_avg_T_RH_P.dat'],'output_avg2','-ascii','-tabs');  % averaged data are saved in the same folder specified in cd
    
    %save in excel format
    T2= table(time_Trhavg,Tavg1,RHavg1,TavgFix, RHavgFix, Pavg);
    writetable(T2,['' num2str(mn) '_sec_avg_T_RH_P.xlsx']);

elseif mn==1   %NO AVERAGE
    Tavg1 = T1;
    RHavg1=RH1; 
    TavgFix = Tfix;
    RHavgFix=RHfix;
    Pavg=P;
    Datetime_Trh_avg=Datetime_Trh;
    time_Trh=[1:1:length(T1)]'; %time in consecutive seconds from the first data point
    
    output_Trh = [time_Trh T1 RH1 Tfix RHfix P];
    save('1_sec_T_RH_P.dat','output_Trh','-ascii','-tabs');  % T/RH data are saved in the same folder specified in cd

    %save in excel format
    T2= table(time_Trh,T1,RH1,Tfix,RHfix,P);
    writetable(T2,'1_sec_T_RH_P.xlsx');
end

%% Import  Liquid-in-Glass T readings 
M = readmatrix('TermLiq.xlsx');  %import Dataset
s=size(M,1); %number of rows
DateTime_liq=datenum([t1(1:3).*ones(s,1),M(:,1:2),zeros(s,1)]); %reconstruc DateTime matrix and convert it into serial date number (Matlab time format)
T_liq=M(:,3); %extract temperature colon

%% Plot sonic temp.(Ts)+ thermohygrom. data (Tair & RH) + Liquid-in-Glass T readings 
disp('***NOTE: in Fig.6 you may want to use instatanueuos values of T1 and RH1 for a better comparison between T1 and in-glass thermometer measures')
figure(6)
yyaxis left
plot(Datetime_Sonic_avg,Tsavg,'-b', 'LineWidth',2)
hold on;
plot(Datetime_Trh_avg,Tavg1,'m','LineStyle','-.','LineWidth',1);
hold on;
plot(Datetime_Trh_avg,TavgFix,'m','LineStyle','-','LineWidth',1);
datetick('x','HH:MM');
legend('Ts','Tair1','Tair (fix)','Orientation','horizontal','Location','bestoutside','FontSize',12);
%---------------------------------------------------------
plot(DateTime_liq,T_liq,'-k.','MarkerSize',10,'LineWidth',1,'DisplayName','Tair(Liq.)') 
%------------------------------------------------------
ylabel(['Temperature [' char(176) 'C]'])
xlabel('time')
yyaxis right
plot(Datetime_Trh, movmean(RH1,mn),'LineWidth',1,'DisplayName','RH1')
plot(Datetime_Trh_avg, RHavgFix,'LineWidth',1,'DisplayName','RHfix')
ylabel('Relat. Humidity [%]')

ax = gca; % current axes
ax.FontSize = 12;

title(['Time Average=', num2str(mn),'s']);

%% Include Ts evaluated as running average
%As figure(6), but using running average (instead of block average)
%to better detect the rapid variations 
disp('***NOTE: in Fig.7 you may want to use instatanueuos values of T1 and RH1 for a better comparison between T1 and in-glass thermometer measures')
figure(6)
figure(7)
yyaxis left
plot(Datetime_Sonic,movmean(Ts,mn),'-','Color',[0.301960796117783 0.745098054409027 0.933333337306976]);
%plot(Datetime_Sonic_avg,Tsavg,'-b', 'LineWidth',2);
hold on;
plot(Datetime_Trh,movmean(T1,mn),'m','LineStyle','-.','LineWidth',1); 

plot(Datetime_Trh,movmean(Tfix,mn),'m','LineStyle','-','LineWidth',1);

datetick('x','HH:MM');
legend('Ts','Tair1','Tair(fixed)','Orientation','horizontal','Location','bestoutside','FontSize',12);
%---------------------------------------------------------
plot(DateTime_liq,T_liq,'-k.','MarkerSize',10,'LineWidth',1,'DisplayName','Tair(Liq.)') %'Color',[0.4940 0.1840 0.5560],'LineWidth',1,'DisplayName','Tair(Liq.)')
%------------------------------------------------------
ylabel(['Temperature [' char(176) 'C]'])
xlabel('time')
yyaxis right
plot(Datetime_Trh, movmean(RH1,mn),'LineWidth',1,'DisplayName','RH1')
plot(Datetime_Trh, movmean(RHfix,mn),'LineWidth',1,'DisplayName','RH(fixed)')
ylabel('Relat. Humidity [%]')
ax = gca; % current axes
ax.FontSize = 12;
title(['MovingAverage=', num2str(mn),'s']);
%%
toc;
