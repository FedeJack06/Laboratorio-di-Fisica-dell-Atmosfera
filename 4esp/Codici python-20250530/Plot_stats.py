# -*- coding: utf-8 -*-
"""
Created on Wed May 14 18:17:38 2025

@author: Erika Brattich (R) & Andrea Faggi (python)
"""

#%% libraries

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

#%%
os.chdir('/home/federico/unibo/atmLab/4esp/')

#filenames = ['stats_box1_orizz', 'stats_box2_orizz', 'stats_box3_orizz', 'stats_image_orizz']
filenames = ['stats_box1_vert', 'stats_box2_vert', 'stats_box3_vert', 'stats_image_vert']
titles = ['Box 1','Box 2','Box 3','Entire image']
for i in range(4):
    filename = filenames[i]
    title = titles[i]
    # open txt
    df = pd.read_csv(filename+'.txt', sep=',')

    # figure and plot
    fig, ax = plt.subplots(figsize=(24,8))

    # background colors and grid 
    #ax.set_facecolor("gainsboro")
    ax.grid(color = "#d0d0d0")

    # add distributon of dataset fields in the plot
    ax.errorbar(df.index, df['Mean [C]'], yerr=df['Std. Dev. [C]'], marker = 'o', mfc='none', label='mean with std')
    ax.plot(df['Maximum [C]'], marker = 's', mfc='none', label='maximum')
    ax.plot(df['Minimum [C]'], marker = '^', mfc='none', label='minimum')

    # set y axis limits
    #ax.set_ylim([24, 34])
    #ax.set_xlim([-2, 252])

    # set x and y axes thicks
    #ax.set_xticks([0.5, 1.0, 2.5, 5.0, 10.0], labels=[0.5, 1.0, 2.5, 5.0, 10.0])
    #ax.set_yticks([0.1, 1.0, 10, 100, 1000], labels=[0.1, 1.0, 10, 100, 1000])

    # add name to x and y axes
    ax.set_xlabel('Frame', fontsize=20) 
    ax.set_ylabel('Temperature [C]', fontsize =20)

    y_min, y_max = ax.get_ylim()
    delta = (y_max - y_min)*0.05

    '''ax.axvline(x=500, color="#353535", linestyle='--')
    ax.text(x=500+8, y=y_max-delta, s='(a)',fontsize=18, va='center', ha='center', color="#353535")#, backgroundcolor='w', zorder=6)
    ax.axvline(x=560, color="#353535", linestyle='--')#, ymin=0.1, ymax=0.9)
    ax.text(x=560+8, y=y_max-delta, s='(b)',fontsize=18, va='center', ha='center', color="#353535")
    ax.axvline(x=600, color="#353535", linestyle='--')
    ax.text(x=600+8, y=y_max-delta, s='(c)',fontsize=18, va='center', ha='center', color="#353535")'''

    ax.axvline(x=240, color="#353535", linestyle='--')
    ax.text(x=240+8, y=y_max-delta, s='(a)',fontsize=18, va='center', ha='center', color="#353535")#, backgroundcolor='w', zorder=6)
    ax.axvline(x=287, color="#353535", linestyle='--')#, ymin=0.1, ymax=0.9)
    ax.text(x=287+8, y=y_max-delta, s='(b)',fontsize=18, va='center', ha='center', color="#353535")
    ax.axvline(x=365, color="#353535", linestyle='--')
    ax.text(x=365+5, y=y_max-delta, s='(c)',fontsize=18, va='center', ha='center', color="#353535")
    ax.axvline(x=490, color="#353535", linestyle='--')
    ax.text(x=490+6, y=y_max-delta, s='(d)',fontsize=18, va='center', ha='center', color="#353535")
    ax.axvline(x=502, color="#353535", linestyle='--')
    ax.text(x=502+6, y=y_max-delta, s='(e)',fontsize=18, va='center', ha='center', color="#353535")

    # add title to the plot
    ax.set_title(title + ' statistics', fontsize =20)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.tick_params(axis='both', which='minor', labelsize=16)

    # add legend
    ax.legend(loc = "upper left", fontsize = 16) 

    # optional function to better manage spaces in the plot
    plt.tight_layout() 

    plt.show()


    # saving plot and closing figure (optional)
    fig.savefig('img/'+filename+'.png', dpi = 300, bbox_inches='tight')
    #plt.close(fig)

    #orizzontale
    #560, 600

    #verticale
    #240, 287, 381-392, 490


