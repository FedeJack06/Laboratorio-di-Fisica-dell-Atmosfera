# -*- coding: utf-8 -*-
"""
Created on Wed May 14 18:17:38 2025

@author: Erika Brattich (R) & Andrea Faggi (python)
"""

#%% libraries

import numpy as np
import pandas as pd
import os

#%% open all

os.chdir('/home/federico/unibo/atmLab/4esp/foglio_verticale_2/')


for i in range(534):
    b = pd.read_fwf('Rec-Vert_2-000001_'+str(i)+' - Stats.txt', widths=[31]*5)
    b.set_index(b['Statistic [units]'], inplace=True, drop=True)

    b = pd.concat([b.loc['Mean [C]'],
                   b.loc['Std. Dev. [C]'],
                   b.loc['Center [C]'],
                   b.loc['Maximum [C]'],
                   b.loc['Minimum [C]'],
                   b.loc['Number of Pixels']], axis=1)
    b = b.T
    b = b.iloc[:,1:5]
    
    if i==0:
        image_temp = pd.DataFrame([b.loc['Mean [C]']['Image'],
                                   b.loc['Std. Dev. [C]']['Image'],
                                   b.loc['Maximum [C]']['Image'][-5:],
                                   b.loc['Minimum [C]']['Image'][-5:]],
                                   index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])
        
        box1_temp = pd.DataFrame([b.loc['Mean [C]']['Box 1'],
                                  b.loc['Std. Dev. [C]']['Box 1'],
                                  b.loc['Maximum [C]']['Box 1'][-5:],
                                  b.loc['Minimum [C]']['Box 1'][-5:]],
                                  index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])
        
        line1_temp = pd.DataFrame([b.loc['Mean [C]']['Box 2'],
                                   b.loc['Std. Dev. [C]']['Box 2'],
                                   b.loc['Maximum [C]']['Box 2'][-5:],
                                   b.loc['Minimum [C]']['Box 2'][-5:]],
                                   index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])
        
        cursor1_temp = pd.DataFrame([b.loc['Mean [C]']['Box 3'],
                                     b.loc['Std. Dev. [C]']['Box 3'],
                                     b.loc['Maximum [C]']['Box 3'][-5:],
                                     b.loc['Minimum [C]']['Box 3'][-5:]],
                                     index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])

        image_sr = image_temp.T
        box1_sr = box1_temp.T 
        line1_sr = line1_temp.T
        cursor1_sr = cursor1_temp.T
 
        
    else:
        image_temp = pd.DataFrame([b.loc['Mean [C]']['Image'],
                                   b.loc['Std. Dev. [C]']['Image'],
                                   b.loc['Maximum [C]']['Image'][-5:],
                                   b.loc['Minimum [C]']['Image'][-5:]],
                                   index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])
        
        box1_temp = pd.DataFrame([b.loc['Mean [C]']['Box 1'],
                                  b.loc['Std. Dev. [C]']['Box 1'],
                                  b.loc['Maximum [C]']['Box 1'][-5:],
                                  b.loc['Minimum [C]']['Box 1'][-5:]],
                                  index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])
        
        line1_temp = pd.DataFrame([b.loc['Mean [C]']['Box 2'],
                                   b.loc['Std. Dev. [C]']['Box 2'],
                                   b.loc['Maximum [C]']['Box 2'][-5:],
                                   b.loc['Minimum [C]']['Box 2'][-5:]],
                                   index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])
        
        cursor1_temp = pd.DataFrame([b.loc['Mean [C]']['Box 3'],
                                     b.loc['Std. Dev. [C]']['Box 3'],
                                     b.loc['Maximum [C]']['Box 3'][-5:],
                                     b.loc['Minimum [C]']['Box 3'][-5:]],
                                     index=['Mean [C]', 'Std. Dev. [C]', 'Maximum [C]', 'Minimum [C]'])
        
        image_temp = image_temp.T
        box1_temp = box1_temp.T
        line1_temp = line1_temp.T       
        cursor1_temp = cursor1_temp.T
               
        image_sr = pd.concat([image_sr, image_temp], ignore_index=True)
        box1_sr = pd.concat([box1_sr, box1_temp], ignore_index=True)
        line1_sr = pd.concat([line1_sr, line1_temp], ignore_index=True)
        cursor1_sr = pd.concat([cursor1_sr, cursor1_temp], ignore_index=True)


del image_temp, box1_temp, line1_temp, cursor1_temp, i

image_sr = image_sr.astype(float)
box1_sr = box1_sr.astype(float)
line1_sr = line1_sr.astype(float)
cursor1_sr = cursor1_sr.astype(float)

# save the dataframe as txt
DIR = '/home/federico/unibo/atmLab/4esp/'
image_sr.to_csv(DIR+'stats_image_vert.txt', sep=',', index=False)
box1_sr.to_csv(DIR+'stats_box1_vert.txt', sep=',', index=False)
line1_sr.to_csv(DIR+'stats_box2_vert.txt', sep=',', index=False)
cursor1_sr.to_csv(DIR+'stats_box3_vert.txt', sep=',', index=False)
