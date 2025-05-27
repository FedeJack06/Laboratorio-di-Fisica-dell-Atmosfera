######## OPC PYTHON PROGRAM ########

#%% Libraries

"""
Here we import all libraries required for the analysis of opc files.
Each library has its own characteristics and functions. Moreover, these are very useful for a wide spectrum of analysis, 
so take notes especially if this is your first approach to pyhton!

For any problems you can contact me at my email: andrea.faggi3@unibo.it

To install a package you can try to open the prompt of your compiler
and type:
    pip install *package name*
"""

import numpy as np                     # This library contains a lot of numerical functions and it is useful for calculations
import os                              # This library allows to set the working directory
import pandas as pd                    # This library allows the data analysis and manipulation of datasets in different formats

import matplotlib as mtp               # This library contains a lot of functions for plotting
import matplotlib.dates as md
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from scipy import stats                # This library allows statistical analysis and it is used here to make data interpolations
from scipy.stats import t              # and to compute statistical distributions
import statsmodels.api as sm

#%% Homemade functions which are similar to openair R package ones

'''
The following is a function to plot your data in a similar way OpenAir scatterPlot does on R. 
Do not change this function in the beginning, but if you want to change some colors or other things do it at your risk.
Anyway, feel free to ask.
'''


def scatterPlot (dataset, var1_name, var2_name, x_axis_name, y_axis_name, saving_name):
    
    # linear regression 
    result = stats.linregress(dataset[var1_name], dataset[var2_name])

    # 95% confidence interval computation
    X = dataset[var1_name]
    Y = dataset[var2_name]
    X = sm.add_constant(X)
    model = sm.OLS(Y,X).fit()
    xseq = pd.Series(np.linspace(np.min(dataset[var1_name]), np.max(dataset[var1_name]), len(dataset[var1_name])))
    xseq_with_const = sm.add_constant(xseq)
    predictions = model.get_prediction(xseq_with_const)
    predicted_values = predictions.predicted_mean
    ci = predictions.conf_int(alpha=0.05)  # ci% = 1 - alpha
  

    # figure and plot
    fig,ax=plt.subplots(constrained_layout=True, figsize=(5,5))

    # background colors and grid 
    ax.set_facecolor("gainsboro")
    ax.grid(color = "white")

    # scatterplot of dataset
    ax.scatter(dataset[var1_name], dataset[var2_name], edgecolors='red', linewidth=0.7, alpha=0.5, facecolors='none', zorder=5)

    # linear regression plot and confidence intervals
    ax.plot(xseq, predicted_values, 'k', zorder=2)
    ax.fill_between(xseq, ci[:,0], ci[:,1], color='g', alpha=0.2)

    # set limits to x and y axes (optional) 
    #ax.set_xlim(left=0)
    #ax.set_ylim(bottom=0)

    # add name to x and y axes
    ax.set_xlabel(x_axis_name)
    ax.set_ylabel(y_axis_name)

    # add results of linear regression (slope, intercept, r^2)
    ax.annotate(var1_name + ' = '+str(np.round(result.slope, 2))+' * ['+ var2_name +'] + '+str(np.round(result.intercept,2))+'; R$^2$ = '+str(np.round(result.rvalue**2,2)), 
                   xy=(0,0), xytext=(0.20,0.94),
                   ha='left', va='center', fontsize=8,
                   xycoords='figure fraction')
    
    # saving plot and closing figure (optional)
    fig.savefig(saving_name, bbox_inches='tight')
    #plt.close(fig)



def timePlot(dataset, time_name, var1_name, label1, var2_name, label2, y_axis_name, saving_name):
    
    # figure and plot
    fig,ax=plt.subplots(constrained_layout=True, figsize=(10,5))

    # background colors and grid 
    ax.set_facecolor("gainsboro")
    ax.grid(color = "white")

    # add timeseries of dataset fields in the plot
    ax.plot(dataset[time_name],dataset[var1_name], 'r', alpha=0.8, zorder=5, label=label1)
    ax.plot(dataset[time_name],dataset[var2_name], 'grey', linestyle='--', zorder=5, label=label2)

    # formatting x axis to have 'hour:minute' format 
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))

    # set limits to x and y axes (optional) 
    #ax.set_xlim(left=0)
    #ax.set_ylim(bottom=0)
    
    # add name to x and y axes
    #ax.set_xlabel(x_axis_name)
    ax.set_ylabel(y_axis_name)

    # add legend (you can change its position by modifying the loc attribute, i.e. 'lower right' or 'left' etc.)    
    ax.legend(ncol=2, loc='upper center', bbox_to_anchor=(0.5, -0.05))
    
    # saving plot and closing figure (optional)
    fig.savefig(saving_name, bbox_inches='tight')
    #plt.close(fig)



def modStats(dataset, obs_name, mod_name, var):
    
    # build a dataset with two columns, one for observations and the other for modeled data
    obs = np.array(dataset[obs_name])
    mod = np.array(dataset[mod_name])
    d = pd.DataFrame({'obs' : obs,
                      'mod' : mod})


    # n: number of complete pairs of obs-mod

    # find rows with nan values
    nan_rows = d.loc[~d.notna().all(axis=1)]
    # remove rows with nan values from dataset
    dn = d.loc[~((d['mod'] == np.nan))]
    # compute number of complete pairs
    n = len(d) - len(nan_rows)
    #print('n = '+str(len(d.obs) - len(nan_rows)))


    # FAC2: fraction within a factor of two
    R = dn['mod']/dn['obs']
    fac2 = len(R.loc[(R > 0.5) & (R < 2)])/len(R)
    #print('FAC2 = ' + str(count))


    # MB: mean bias
    res = (dn['mod'] - dn['obs'])/len(d['obs'])
    mbe = res.sum()
    #print('MB = ' + str(mbe))


    # MGE: mean gross error
    res = (dn['mod'] - dn['obs'])/len(dn['obs'])
    res = np.abs(res)
    mge = res.sum()
    #print('MGE = ' + str(mge))


    # NMB: normalized mean bias
    res = (dn['mod'] - dn['obs'])/dn['obs'].sum()
    nmb = res.sum()
    #print('NMB = ' + str(nmb))


    # NMGE: normalized mean gross error
    res = np.abs(dn['mod'] - dn['obs'])/dn['obs'].sum()
    nmge = res.sum()
    #print('NMB = ' + str(nmb))


    # RMSE: Root Mean Squared Error
    res = np.mean((dn['mod'] - dn['obs'])**2)**0.5
    rmse = res.sum()
    #print('RMSE = ' + str(rmse))


    # r: Pearson's coefficient; p: p value
    correlation, p_value = stats.pearsonr(dn['mod'], dn['obs'])
    #print('r = ' + str(correlation))
    #print('p value = ' + str(p_value))


    # COE: Coefficient of Efficiency based on Legated and McCabe (1999, 2012)
    num = np.abs(dn['mod'] - dn['obs'])
    num = num.sum()
    den = np.abs(dn['obs'] - np.ones(len(dn['obs']))*dn['obs'].mean())
    den = den.sum()
    coe = 1 - num/den
    #print('COE = ' + str(coe))

    # IOA: Index of agreement based on Willmott (2011)
    LHS = np.abs(dn['mod'] - dn['obs'])
    LHS = LHS.sum()
    RHS = np.abs(dn['obs'] - np.ones(len(dn['obs']))*dn['obs'].mean())
    RHS = 2*RHS.sum()
    if LHS <= RHS:
        ioa = 1 - LHS/RHS
    else:
        ioa = RHS/LHS - 1
    #print('IOA = ' + str(ioa))

    # collecting all statistical variables computed into a single dataframe
    res = pd.DataFrame({var : [n, fac2, mbe,
                        mge, nmb, nmge,
                        rmse, correlation,
                        p_value, coe, ioa]},
                        index = ['n', 'fac2', 'mbe', 'mge',
                                     'nmb', 'nmge', 'rmse', 'r',
                                     'p_value', 'coe', 'ioa'])

    # return the dataframe
    return res

def summary(df, file_name, sep='\t', dec='.', col_names=True, row_names=True):
    
    # build a dataset to store all statistics with proper dimensions and indexes
    a = df.shape[1]
    index = ['Min', '1st Q', 'Median', 'Mean', '3rd Q', 'Max']
    sta_df = pd.DataFrame(np.zeros((6,a)), index=index, columns=df.columns)

    # statistics computation
    for i in range(a):
        for j in range(6):
            if j==0: sta_df.iloc[j,i] = df.iloc[:,i].min()
            elif j==1: sta_df.iloc[j,i] = np.percentile(df.iloc[:,i], q=25)
            elif j==2: sta_df.iloc[j,i] = np.percentile(df.iloc[:,i], q=50)
            elif j==3: sta_df.iloc[j,i] = df.iloc[:,i].mean()
            elif j==4: sta_df.iloc[j,i] = np.percentile(df.iloc[:,i], q=75)
            elif j==5: sta_df.iloc[j,i] = df.iloc[:,i].max()

    # save the dataset as txt file
    sta_df.to_csv(file_name, sep=sep, decimal=dec, header=col_names, index=row_names)

    return sta_df

def ttest(x1, x2, eq_var, cl=0.95):
       
    # Welch Two Sample t-test 
    t_test = stats.ttest_ind(x1, x2, alternative = "two-sided", equal_var = eq_var)

    # computing mean and standard deviation of each variable
    mu1 = np.mean(x1)
    mu2 = np.mean(x2)
    std1 = np.std(x1, ddof=1)
    std2 = np.std(x2, ddof=1)
    n1 = len(x1)
    n2 = len(x2)

    # Calculate the standard error of the difference between means
    se_diff =  np.sqrt((std1**2 / n1) + (std2**2 / n2))

    # Calculate the t-statistic for the 95% confidence level
    new_cl = 1 - cl
    t_critical = stats.t.ppf(1 - new_cl/2, t_test.df)  # 95% CI means 0.025 in each tail

    # Calculate the margin of error
    margin_of_error = t_critical * se_diff

    # Calculate the confidence interval
    mean_diff = mu1 - mu2
    lower_bound = mean_diff - margin_of_error
    upper_bound = mean_diff + margin_of_error

    # collecting all statistical variables computed into a single dataframe
    res = pd.DataFrame({'var' : [t_test.statistic, t_test.df, t_test.pvalue,
                               mu1, std1, n1, mu2, std2, n2,
                               lower_bound, upper_bound]},
                        index = ['t', 'df', 'p-value',
                                 'mean x1', 'std x1', 'n x1', 'mean x2', 'std x2', 'n x2',
                                 '95perc c.i. lb', '95perc c.i. ub'])
    
    # print statistical information
    print('Welch Two Sample t-test')
    print('t = '+str(np.round(res.loc['t'].item(), 4)))
    print('df = '+str(np.round(res.loc['df'].item(), 3)))
    print('p-value = '+str(np.round(res.loc['p-value'].item(), 3)))
    print()
    print(str(cl*100)+' percent confidence interval:')
    print('lower bound = '+str(np.round(res.loc['95perc c.i. lb'].item(), 5)))
    print('upper bound = '+str(np.round(res.loc['95perc c.i. ub'].item(), 5)))
    print()
    print('sample estimates (mean, std, n):')
    print('x1: ('+str(np.round(res.loc['mean x1'].item(), 3))+', '+str(np.round(res.loc['std x1'].item(), 3))+', '+str(res.loc['n x1'].item())+')') 
    print('x2: ('+str(np.round(res.loc['mean x2'].item(), 3))+', '+str(np.round(res.loc['std x2'].item(), 3))+', '+str(res.loc['n x2'].item())+')') 

    # return the dataframe
    return res


'''
In this first part we have prepared the libraries we will use in the following part of the program. 
Now the real programming part starts!
'''

#%% Set variables

"""
This part is dedicated to the process of reading measuerements and preparing the dataset
for further analysis. Pay attention to every passage.
"""

# Set working directory, change as appropriate
os.chdir('C:/Users/andre/Desktop/Assegno/Tutoraggio/')


# Read data table, skip first two lines after 
file_name = '20-10-14_prove.csv'
datos = pd.read_csv(file_name, sep=',', header=0, skiprows=2)

'''
Here we remove the first line since it contains sample data.
Then we reset the index of the dataframe. 
You have to do this everytime a row is removed from a dataframe opened with pandas library.
'''

# removing the first row from datos dataframe
datos = datos.iloc[1:,:]

# resetting datos dataframe index 
# (drop=True does not allow the old index to be added as a new column)
datos = datos.reset_index(drop=True)

'''
Now we have to fix the "Time" column of our dataframe.
'''


# In the "Time" column, substitute T with a space and remove Z
datos['Time'] = datos['Time'].str.replace('T',' ')
datos['Time'] = datos['Time'].str.replace('Z','')

# Read the "Time" as date, specifying the format
datos['Time'] = pd.to_datetime(datos['Time'], format = '%Y-%m-%d %H:%M:%S', utc = True)

'''
Now the dataset is ready to be elaborated and analysed.
'''


#%% Data treatment and analysis 1

"""
In our first step we want to convert particle counts to PM [micrograms/m-3]. Pay attention to the units:
- Particle density is given in g cm-3
- Diameter is in micrometers

The particle numbers in the respective size bins are divided by 0.1 L (flow rate).
Create the matrices wich will contain the data, now filled with NAs.
"""

# Create a matrix of 1 rowm 7 columns containing the size bins in the first row (header)
bin_opc = np.array([0.3, 0.5, 1.0, 2.5, 5.0, 10.0, 15.0])


# Create a matrix of diameters of the counter, all 0s for now, 1 row and 6 columns
# NOTE: the matrix has 1 column less than the size bins
D_opc = np.zeros(6)


# Create a matrix of 0s, same number of rows as datos (your data) and 6 columns
# NOTE: the matrix has the same number of columns as D_opc
m_opc = np.zeros( (len(datos.iloc[:,1]), 6) )


# Name the columns of m_opc pasting the text "bin", a sequence of nubers from 1 to 6
# and the text "_opc"
m_opc = pd.DataFrame(m_opc)
m_opc.columns = ["bin" + str(i) + "_opc" for i in range(0,6)]


# Extract the portion of datos (your data) containing the particle counts
# Conversion of counts/0.1 L to counts/cm3
opc_s = datos.iloc[:,12:18] * 10**(-3)


# for loop: for each size bin, calculate the Lower Bound (LB), the Upper Bound (UB),
# the Diameter (D), and finally the mass (m)
for i in range(0,6):
    LB = bin_opc[i]
    UB = bin_opc[i+1]
    D_opc[i] = LB*(1/4*(1+(UB/LB)**(2))*(1+(UB/LB)))**(1/3)
    m_opc.iloc[:,i] = 1.65*opc_s.iloc[:,i]*(D_opc[i]*10**(-4))**(3)*np.pi/6


# Calculate the concentrations in micrograms/m3 for each size bin
C_opc = m_opc * 10**13


# Calculate PM mass concentrations summing up the appropriate size bins
# PM1
pm1 = C_opc.iloc[:,0:2].sum(axis=1)

# PM2.5
pm25 = C_opc.iloc[:,0:3].sum(axis=1)

# PM10
pm10 = C_opc.iloc[:,0:5].sum(axis=1)

# Add to datos all PMs calculated and change relative columns names
datos = pd.concat([datos, pm1, pm25, pm10], axis=1)
datos = datos.rename(columns={0: 'pm1',
                              1: 'pm2.5',
                              2: 'pm10'})


#%% Scatterplots

'''
Here we compare data we have just calculated to those automatically retrieved by the sensor. 
This analysis is useful to see if the algorithm we adopted is consistent with the one used by the instrument, and ultimately to evaluate the bias between the two outputs.

Note that the bias can be different for different PM fractions.

This comparison can be performed throigh a scatter plot.
In our case we use the function scatterPlot(), that is built here to give the same output as the homonymus function belonging to the R library openAir.

Note that these functions save the plot in your working directory in the specified format, i.e. if you use 'PM1_plot.png' the chart will be saved in png format, you can try also with jpg, pdf and other formats as well.
'''

scatterPlot(datos, 'PM 1.0', 'pm1', 'Measured PM$_1$ ($\\mu g/ m^3$)', 'Calculated PM$_1$ ($\\mu g/ m^3$)', 'PM1_plot.png')
scatterPlot(datos, 'PM 2.5', 'pm2.5', 'Measured PM$_{2.5}$ ($\\mu g/ m^3$)', 'Calculated PM$_{2.5}$ ($\\mu g/ m^3$)', 'PM25_plot.png')
scatterPlot(datos, 'PM 10.0', 'pm10', 'Measured PM$_{10}$ ($\\mu g/ m^3$)', 'Calculated PM$_{10}$ ($\\mu g/ m^3$)', 'PM10_plot.png')


#%% Time series plots

'''
Now we use the time series plots to compare the PM data. 
In this way we can evaluate if thw bias is constant, of if instead it changes in time. 
We also can note hoe the PM concentrations changed uring the experience.

We uset the timePlot() function, which is built here to give the same output as the homonymus function belonging to the R library openAir.

Note that these function save the plots in the same way scatterPlot does.
'''

timePlot(datos, 'Time', 'PM 1.0', 'measured PM$_{1}$', 'pm1', 'calculated PM$_{1}$', 'PM$_{1}$ ($\\mu g ~ m^{-3}$)', 'time_pm1.png')
timePlot(datos, 'Time', 'PM 2.5', 'measured PM$_{2.5}$', 'pm2.5', 'calculated PM$_{2.5}$', 'PM$_{2.5}$ ($\\mu g ~ m^{-3}$)', 'time_pm25.png')
timePlot(datos, 'Time', 'PM 10.0', 'measured PM$_{10}$', 'pm10', 'calculated PM$_{10}$', 'PM$_{10}$ ($\\mu g ~ m^{-3}$)', 'time_pm10.png')


#%% Comparison statistics

'''
We now also evaluate the comparison using appropriate statistical indicators. To calculate them, we use the modStats() function which calculates common numerical model evaluation statistics. This includes: 
- n, the number of complete pairs of data. 
- FAC2, fraction of predictions within a factor of two.
- MB, the mean bias. * MGE, the mean gross error. 
- NMB, the normalised mean bias. 
- NMGE, the normalised mean gross error. 
- RMSE, the root mean squared error. 
- r, the Pearson correlation coefficient. 
- COE, the Coefficient of Efficiency based on Legates and McCabe (1999, 2012). 
- IOA, the Index of Agreement based on Willmott et al. (2011), which spans between -1 and +1 with values approaching +1 representing better model performance. 
All statistics are based on complete pairs of mod (in our case, the calculated PM) and obs (in our case, the PM data retrieved directly by the sensor). 
NOTE: the list is rather complete, but you can consider to add the calculation of other parameters, using commands you used in other Experiences (e.g., Esperienza 3).

We now use again the pd.concat() function to merge the calculated statisitical parameters to a single dataframe. 
We then write the parameters for the three PM size fractions to a .txt file through the df.to_csv() function (df is the name of the dataframe).
This function prints the dataframe to a file or connection. The arguments specify that we want to use the decimal point, the tab as separation, column names but not row names.
'''

# computation of statistical values for each PMx
stat_pm1 = modStats(datos, 'PM 1.0', 'pm1', 'PM_1')
stat_pm25 = modStats(datos, 'PM 2.5', 'pm2.5', 'PM_2.5')
stat_pm10 = modStats(datos, 'PM 10.0', 'pm10', 'PM_10')

# collecting all statistical values into a single dataframe
stat_PM = pd.concat((stat_pm1, stat_pm25, stat_pm10), axis = 1)

# save the dataframe as txt
stat_PM.to_csv('stat_PM.txt', sep=',')

'''
We calculate also the Spearman correlation correlation coefficient. 
This coefficient is a non-parametric statistical measure of correlation, which measures the degree of correlation between two variables but without assuming that the relationship between them is linear. 
For this we first extract a single portion of data to be compared, and then use the stat.spearmanr() function to calculate the correlation. 
We finally use again the pd.concat() function to write the results to a .txt file in the working directory.
'''

# selecting proper dataset columns
data_manual = datos.iloc[:, 18:22]
data_autom = datos.iloc[:, 9:12]

# calculation of the spearman r
corr = stats.spearmanr(data_manual, data_autom)
spear = pd.DataFrame(corr[0])

# selecting only the proper column (stats.spearmanr provides a 6x6 simmetri matrix, we need only a part of it)
spear = spear.iloc[0:3, 3:]

# setting the index of the dataframe
spear = spear.set_index(pd.Index(['pm1', 'pm2.5', 'pm10']))

# renamning the names of the columns
spear = spear.rename(columns={3: "PM 1.0", 4: "PM 2.5", 5: "PM 10.0"})

# save the dataframe as txt
spear.to_csv('spearman_corr.txt', sep=',')


#%% Comparison of particle distributions

'''
Comparison of particle distributions during different phases (locations) of the experience We now evaluate the difference in the particle distributions acquired by the sensor during the different phases (locations) of the experience. 

Firstly, we need to define the subsets for the different phases.
We will do so by selecting the specific timesteps in the dataframe index, specifying directly the date and times of the different phases.

Here we select the part of dataset which belogns to a phase of the experiment.
The selection can be done by asking to our dataframe to select only the timesteps belonging to a specific range. 
This can be done in the following way (after setting as index of our dataframe the timestep column):

    dataframe.loc['start_time':'end_time']

The ':' means for python to take into account every row in between the two extremes.

In the following example I asked to take all rows between 08:19 and 08:49 of the datos dataframe, and save it in the subdata1 variable.
And accordingly I created a second phase variable for a different time range.

Remember to change date and time as appropriate.
'''

# setting the column named 'Time' as the index of the dataframe
datos.set_index(datos['Time'], inplace=True)

# selecting data using the index and the datetime format
subdata1 = datos.loc['2020-10-14 08:19:00':'2020-10-14 08:49:00']
subdata2 = datos.loc['2020-10-14 09:00:00':'2020-10-14 09:30:00']

# removing the first column from the dataset
subdata1 = subdata1.iloc[:, 1:]
subdata2 = subdata2.iloc[:, 1:]

'''
We have to calculate the temporal mean of the data acquired during the different phases. 
We will use a pandas functionaility wich allows the calculation of different kinds of time average. 
This function is useful to aggregate or expand data frames by different time periods, calculating vector-averaged wind direction where appropriate.
The averaged periods can also take account of data capture rates.
Consequently, we will save the averaged data for the different phases to a .txt file. 

NOTE: again, if you have a third phase in your experience, you need to repeat the commands.
'''

#datos_first = subdata1.rolling('30min', center=True).mean()
#datos_second = subdata2.rolling('30min', center=True).mean()

# computing the mean value for each dataset
datos_first = subdata1.mean()
datos_second = subdata2.mean()

# save the dataframe as txt
datos_first.to_csv('first period average.txt', sep=',')
datos_second.to_csv('second period average.txt', sep=',')

'''
We extract particle number data from the two subsets. 
Here we convert the particle counts into particle numerical concentration, so the unit changes from # to #/cm3.
'''

flow_rate = 0.01 * 10**(3)   #flow rate in L to flow rate in cm3

PN1 = datos_first.iloc[11:17]/flow_rate
PN2 = datos_second.iloc[11:17]/flow_rate

'''
We now plot the average particle size distributions in the two phases to compare them. 
To do so, we want to plot the two (or more, if needed) distributions on the same graph. 
We first plot the distribution for the first phase, using a log scale for both x and y axes.
Then we add the plot for the second phase on the same graph. 
We then add the tick labels (need to be modified), and finally add the legend. 

Since the y-axis range of the plots are not necessarily the same, we also specify the same ranges for all the plots.
Note: as done above, the plots will be produced directly on the right screen of the IDE program (Spyder or VSC) and you can save it through the Export command. 
If you wish to directly save it on a png file, add the appropriate commands.
'''

# figure and plot
fig, ax = plt.subplots(figsize=(10,7))

# background colors and grid 
ax.set_facecolor("gainsboro")
ax.grid(color = "white")

# add distributon of dataset fields in the plot
ax.plot(D_opc, PN1, marker = 'o', mfc='none', label='first subset')
ax.plot(D_opc, PN2, marker = 'o', mfc='none', label='second subset')

# set a logaritmic scale on the x and y axes
ax.set_yscale('log')
ax.set_xscale('log') 

# set y axis limits
ax.set_ylim(0.01, 200)

# set x and y axes thicks
ax.set_xticks([0.5, 1.0, 2.5, 5.0, 10.0], labels=[0.5, 1.0, 2.5, 5.0, 10.0])
ax.set_yticks([0.1, 1.0, 10, 100, 1000], labels=[0.1, 1.0, 10, 100, 1000])

# add name to x and y axes
ax.set_xlabel('Bin mean diameter ($\\mu m$)') 
ax.set_ylabel('dN/dln(D) ($cm^{-3}$)')

# add legend
ax.legend(loc = "upper right") 

# optional function to better manage spaces in the plot
plt.tight_layout() 

# saving plot and closing figure (optional)
#fig.savefig(saving_name, bbox_inches='tight')
#plt.close(fig)

'''
We obtain the average particle surface distributions for the two (or more) phases, and repeat the same steps to produce the graph.
'''

# computing surfaces under spherical particle hypothesis 
S_opc = np.pi * D_opc**2

# particle surface distribution for each stage of the experiment
PS1 = S_opc * PN1
PS2 = S_opc * PN2


# figure and plot
fig, ax = plt.subplots(figsize=(10,7)) 

# background colors and grid 
ax.set_facecolor("gainsboro")
ax.grid(color = "white")

# add distribution of dataset fields in the plot
ax.plot(D_opc, PS1, marker = 'o', mfc='none', label='first subset')
ax.plot(D_opc, PS2, marker = 'o', mfc='none', label='second subset')

# set a logaritmic scale on the x and y axes
ax.set_yscale('log')
ax.set_xscale('log')

# set y axis limits
ax.set_ylim(1, 100)

# set x and y axes thicks
ax.set_xticks([0.5, 1.0, 2.5, 5.0, 10.0], labels=[0.5, 1.0, 2.5, 5.0, 10.0])
ax.set_yticks([1.0, 10, 100], labels=[1.0, 10, 100])

# add name to x and y axes
ax.set_xlabel('Bin mean diameter ($\\mu m$)') 
ax.set_ylabel('dS/dln(D) ($ \\mu m^2 /  cm^{-3}$)')

# add legend
ax.legend(loc = "upper right") 

# optional function to better manage spaces in the plot
plt.tight_layout() 

# saving plot and closing figure (optional)
#fig.savefig(saving_name, bbox_inches='tight')
#plt.close(fig)

'''
We obtain the average particle volume distributions for the two (or more) phases, and repeat the same steps to produce the graph.
'''

# computing volumes under spherical particle hypothesis 
V_opc = np.pi/6 * D_opc**3

# particle volume distribution for each stage of the experiment
PV1 = PN1 * V_opc
PV2 = PN2 * V_opc

# figure and plot
fig, ax = plt.subplots(figsize=(10,7)) 

# background colors and grid 
ax.set_facecolor("gainsboro")
ax.grid(color = "white")

# add distribution of dataset fields in the plot
ax.plot(D_opc, PV1, marker = 'o', mfc='none', label='first subset')
ax.plot(D_opc, PV2, marker = 'o', mfc='none', label='second subset')

# set a logaritmic scale on the x and y axes
ax.set_yscale('log')
ax.set_xscale('log') 

# set y axis limits
ax.set_ylim(1, 100)

# set x and y axes thicks
ax.set_xticks([0.5, 1.0, 2.5, 5.0, 10.0], labels=[0.5, 1.0, 2.5, 5.0, 10.0])
ax.set_yticks([1.0, 10, 100], labels=[1.0, 10, 100])

# add name to x and y axes
ax.set_xlabel('Bin mean diameter ($\\mu m$)') 
ax.set_ylabel('dV/dln(D) ($ \\mu m^3 /  cm^{-3}$)')

# add legend
ax.legend(loc = "upper right") 

# optional function to better manage spaces in the plot
plt.tight_layout()

# saving plot and closing figure (optional)
#fig.savefig(saving_name, bbox_inches='tight')
#plt.close(fig)

'''
We can also calculate the mean and standard deviation using the mean and sd functions. 
Here they are calculated for particle counts in the 0.3 micron size bin, but if you need you can change this as appropriate.
'''

# find mean for the particle number in 0.3 micron bin; change as appropriate
period1_mu03 = np.mean(subdata1['PN 0.3'])
period2_mu03 = np.mean(subdata2['PN 0.3'])

# find standard deviation for the particle number in 0.3 micron bin
period1_sd03 = np.std(subdata1['PN 0.3'])
period2_sd03 = np.std(subdata2['PN 0.3'])


# Calculate summary statistics to compare the two phases. Repeat if necessary.
# Note: the summary function also saves the dataset as a txt table.
sta_period1 = summary(subdata1, 'first period summary statistics.txt', sep='\t', dec='.', col_names=True, row_names=True)
sta_period2 = summary(subdata2, 'second period summary statistics.txt', sep='\t', dec='.', col_names=True, row_names=True)

#%% Data distribution

'''
Visualization of the data distribution for the 2 locations

First, we will plot the counts with histograms. Then, we will plot the normal distribution, which mimics t-distribution when sample number (N) is large.
To visualize the normal distribution, we should know: 
- The sample mean; 
- Sample standard deviation; 

We can also use the function ‘stats.gaussian_kde(x)’ to plot the probability density against x, and the PM values in different locations. 
Then, visually, we can see in one figure that difference between the 2 places, how much is the difference between their mean PM values and what is the extent of # deviation of the PM (particle counts) measurements in each location. 
Firstly we define the bin width for the histogram.
We then calculate the sum of the rows corresponding to the particle counts in the two phases.
And then we calculate the means and standard deviation of those sums in the two periods (locations).
'''

# sum number concentration for each timestep in the two steps of the experiment
sum_first = subdata1.iloc[:,11:17].sum(axis=1)
sum_second = subdata2.iloc[:,11:17].sum(axis=1)

# compute the means of the two phases of the experiment
period1_mu = sum_first.mean()
period2_mu = sum_second.mean()

# compute the standard deviation of the two phases of the experiment
period1_sd = np.std(sum_first, ddof=1)
period2_sd = np.std(sum_second, ddof=1)

'''
Let’s make the plot. 
First we call the function and then each function is dedicated to a specific graphic command.
'''

# figure and plot
fig, ax = plt.subplots(tight_layout=True,figsize=(10.0,7.0))

# background colors and grid 
ax.set_facecolor("gainsboro")
ax.grid(color = "white")

# histograms, bins can be either automatically determined or passed to the function with the bins attribute
ax.hist(sum_second, bins=np.linspace(800, 2000, 25), color="#d8b365", edgecolor='white', alpha = 1, zorder=2)
ax.hist(sum_first, bins=np.linspace(800, 2000, 25), color="#5ab4ac", edgecolor='white', alpha = 0.6, zorder=3)

# compute probability density functions
density1 = stats.gaussian_kde(sum_first)
density2 = stats.gaussian_kde(sum_second)
x = np.arange(800, 2000, 0.1)
ax.plot(x, 2500*density1(x), zorder=4, color = 'b') # Multiplied by 2500 for visualisation only
ax.plot(x, 2500*density2(x), zorder=5, color = 'r') # Multiplied by 2500 for visualisation only

# add name to x and y axes
ax.set_xlabel('Total PM with d > 0.3 $\\mu m$ per 0.1 L')
ax.set_ylabel('Counts')

# add title to the plot
ax.set_title('> 0.3 $\\mu  m$ PM Count')

# add legend
s1 = mpatches.Patch(color="#5ab4ac", alpha = 0.6, label='First subset')
s2 = mpatches.Patch(color="#d8b365", alpha = 1, label='Second subset')
s3 = mpatches.Patch(color="#8CB38F", alpha = 0.6, label='Overlapping regions')
ax.legend(handles=[s1, s2, s3])

# optional function to better manage spaces in the plot
plt.tight_layout()

# saving plot and closing figure (optional)
#fig.savefig(saving_name, bbox_inches='tight')
#plt.close(fig)


'''
We then plot the normal distribution. 
To do so, we make use of the stats.norm.pdf() function.
First we need to calculate the data that then will be visualized. 
To do so, we make use of the stats.norm.pdf() function and of the observed mean and standard deviation for the two locations.
'''

# computing the normal distribution given mean and standard deviation of the first dataset
x1norm = np.linspace(period1_mu - period1_mu/2, period1_mu + period1_mu/2, 1001)
y1norm = stats.norm.pdf(x1norm, loc = period1_mu, scale = period1_sd)
first_ydnorm = pd.DataFrame({'x1' : x1norm, 'y1_norm' : y1norm})

# computing the normal distribution given mean and standard deviation of the second dataset
x2norm = np.linspace(period2_mu - period2_mu/2, period2_mu + period2_mu/2, 1001)
y2norm = stats.norm.pdf(x2norm, loc = period2_mu, scale = period2_sd)
second_ydnorm = pd.DataFrame({'x2' : x2norm, 'y2_norm' : y2norm})

'''
We can now produce the plot.
First we reset the bin width and then we plot the normally distributed data that we just obtained.
'''

# figure and plot
fig, ax = plt.subplots(tight_layout=True,figsize=(10.0,7.0))

# background colors and grid 
ax.set_facecolor("gainsboro")
ax.grid(color = "white")

# histograms, bins can be either automatically determined or passed to the function with the bins attribute
# since the attribute density is set true counts are normalized over the total occurrences
ax.hist(sum_second, bins=np.linspace(800, 2000, 25), color="r", density = True, edgecolor='white', alpha = 0.6, zorder=2)
ax.hist(sum_first, bins=np.linspace(800, 2000, 25), color="b", density = True, edgecolor='white', alpha = 0.5, zorder=3)

# normal probability density functions plots
ax.plot(first_ydnorm.x1, first_ydnorm.y1_norm, zorder=4, color = 'b')
ax.plot(second_ydnorm.x2, second_ydnorm.y2_norm, zorder=5, color = 'r')

# vertical lines representing the mean of each dataset
ax.plot([period1_mu, period1_mu], [0, 1], linestyle = '--', color='blue', zorder = 6)
ax.plot([period2_mu, period2_mu], [0, 1], linestyle = '--', color='red', zorder = 6)

# set y axis limits
ax.set_ylim([0, 0.00375])

# add name to x and y axes
ax.set_xlabel('Total PM with d > 0.3 $\\mu m$ per 0.1 L')
ax.set_ylabel('Normalized counts')

# add title to the plot
ax.set_title('> 0.3 $\\mu  m$ PM Count Probability Density')

# add legend
s1 = mpatches.Patch(color="b", alpha = 0.6, label='First subset')
s2 = mpatches.Patch(color="r", alpha = 0.6, label='Second subset')
s3 = mpatches.Patch(color="#772BAB", label='Overlapping regions')
ax.legend(handles=[s1, s2, s3])

# optional function to better manage spaces in the plot
plt.tight_layout() 

# saving plot and closing figure (optional)
#fig.savefig(saving_name, bbox_inches='tight')
#plt.close(fig)

#%% t-test

'''
In this section, we are going to perform hypothesis test on the PM data we obtain in different locations (say, courtyard & bus stop), to test if the PM data in courtyard is either significantly greater, less, or different from the PM data at the bus stop. 
We are going to use t-test, a statistical inference tool to do our hypothesis test. 
Because we are interested to know if the mean values of the courtyard are significantly different than those at the bus stop, we set the alternative hypothesis to ask whether the mean for Place 1 (courtyard) is different than for Place 2 (bus stop). 
The confidence level is set at 0.95.
'''


'''
Computing all statistical values for the t-test. With cl you can set the confidence level, eq-var set false means that the two 
sets of data have different variance. This function provides a two-sided t-test.
'''
t_test_PM = ttest(sum_first, sum_second, cl = 0.95, eq_var = False)

# save the dataframe as txt
t_test_PM.to_csv('ttest_results.txt', sep=',')



'''
Here we plot our t-distributions for our t-tests, inputs are:
- T Probability Density = t.pdf(x, df), where x is a vector of t-values (we can imagine that t-value is the normalized mean value of our data) where df is the Degree of Freedom (df=t_test_PM.loc['df']), which has been calculated using the ttest() function 
- Critical t-value for the t-test, which defines as crit_val = t.ppf(.95, df=t_test_PM.loc['df']) 
- t-value, defined as t_test_PM.loc['t'] which has been calculated in our t-test as well. 

Similar as what we do above, to perform our t-test visually, we want to compare the t-value and critical t-value – if |t-value| is greater than |critical t-value|, we reject the null hypothesis.

First we calculate the values and the intervals.
'''


# creating a vector of x data
x_t = pd.DataFrame(np.linspace(-6, 6, 1000), columns=['x']) # replaced len(subset1) with 1000 tp have a smoother t-test chart

# calculating the probability density function using the x vector
y_t = pd.DataFrame(t.pdf(x_t, df=t_test_PM.loc['df']), columns=['y'])

# creating a dataset for x and y of the probability density function
t_test = pd.concat([x_t, y_t], axis=1)

# computing the critical values for the t-test, note that it is two-sided so we have to consider higher and lower parts of the distribution
crit_val_hi = t.ppf(0.975, df=t_test_PM.loc['df'])
crit_val_lo = t.ppf(0.025, df=t_test_PM.loc['df'])

# creating a dataframe to compute the shaded area in the higher part of distribution
shade1 = pd.concat([pd.DataFrame({'x' : [crit_val_hi.item()], 'y' : [0]}),
                    t_test.loc[t_test.x > crit_val_hi.item()],
                    pd.DataFrame({'x' : [np.inf], 'y' : [0]})], ignore_index=True)

# creating a dataframe to compute the shaded area in the lower part of distribution
shade2 = pd.concat([pd.DataFrame({'x' : [-np.inf], 'y' : [0]}),
                    t_test.loc[t_test.x < crit_val_lo.item()],
                    pd.DataFrame({'x' : [crit_val_lo.item()], 'y' : [0]})], ignore_index=True)



'''
We then plot the results again by using matplotlib library and a series of graphic commands to make the plot nice.
'''

# figure and plot
fig, ax = plt.subplots(tight_layout=True,figsize=(10.0,7.0))

# background colors and grid 
ax.set_facecolor("gainsboro")
ax.grid(color = "white")

# create the t distribution plot
ax.plot(t_test.x, t_test.y, zorder=4, color = 'k')

# fill the shaded areas defined by the higher and lower critical values of t-test
ax.fill_between(shade1.x, np.zeros(len(shade1)), shade1.y, color='red', alpha = 0.6)
ax.fill_between(shade2.x, np.zeros(len(shade2)), shade2.y, color='red', alpha = 0.6)

# creating the vertical line representing the 0
ax.plot([0, 0], [0, 0.5], color='r', alpha= 0.5, zorder = 6)

# add vertical line representing the t-test critical value found
ax.plot([t_test_PM.loc['t'], t_test_PM.loc['t']], [0, 0.5], color='b', linewidth = 3, zorder = 6)

# add title to the plot
ax.set_title('T-test Results')

# add name to x and y axes
ax.set_xlabel('t-value')
ax.set_ylabel('Density')

# set x and y axes limits
ax.set_ylim([0, 0.42])
ax.set_xlim([-7, 7])

# optional function to better manage spaces in the plot
plt.tight_layout()

# saving plot and closing figure (optional)
fig.savefig('t-test', bbox_inches='tight')
#plt.close(fig)


#%% Optional part: calculate the moments

'''
As a final and optional point, we will calculate the moments of the particle size distributions for the phases of the experience. 
We have two options: either we apply the direct calculation (maybe defining a function), either we make use of the formulae given on the right of slide 89.
Let’s use the formulae given on the right.
'''
# moment of order zero is just the total number of particles (convert back to # particles)
totPN1 = PN1.sum() * 10
totPN2 = PN2.sum() * 10

# moment of order one is the average particle diameter multiplied the moment of order zero
mean_diam = D_opc.mean()
mom1_1 = totPN1 * mean_diam
mom1_2 = totPN2 * mean_diam

# moment of order two is the average surface area multiplied the moment of order zero and divided by pi
mean_area = np.pi * mean_diam**2
mom2_1 = mean_area * totPN1 / np.pi
mom2_2 = mean_area * totPN2 / np.pi

# moment of order three is the average volume multiplied six times the moment of order zero and divided by pi
mean_vol = np.pi/6*mean_diam**3
mom3_1 = mean_vol * 6 * totPN1/np.pi
mom3_2 = mean_vol * 6 * totPN2/np.pi