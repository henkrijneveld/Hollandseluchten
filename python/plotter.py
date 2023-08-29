import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime
import seaborn as sns
import sys
import os
import pprint as pp
import math

from analyzer import *

# difplot on attribute name
def diffPlot(leftframe, rightframe, attr):
    deltas = diffFrame(leftframe, rightframe, attr)
    lplot = sns.histplot(data=deltas, x="delta_"+attr, binwidth=0.50, kde=True)
    lplot.set(xlim=(-40.0, 20.0))
    plt.show()
    return

def windplot(frame, values, polar=True, useMedian=True):
    conc = weatherFrame(frame)
    conc = medianvalues([conc], "winddirection", values)
    if not useMedian:
        values = values + "_mean"
    if polar:
        conc["winddirection"] = conc["winddirection"] / 180 * math.pi
        conc.drop(index=37, inplace=True) # this is value 990: variable winds
        conc.loc[0] = conc.loc[36].copy() # direction 0: no wind
        conc["winddirection"][0] = 0
        g = sns.FacetGrid(conc, subplot_kws=dict(projection='polar', theta_offset=math.pi/2, theta_direction=-1), height=10,
                          sharex=False, sharey=False, despine=False)
        g.map_dataframe(sns.lineplot, x="winddirection", y=values, linewidth=4.0)
    else:
        lplot = (sns.scatterplot(data=conc, x="winddirection", y=values))
        lplot.set(xlim=(5.0, 365.0))
    plt.show()

def windhistogram(frame, polar=True):
    conc = frame.groupby("winddirection").count()
    conc = conc.reset_index()
    conc.columns.values[0] = "winddirection"
    if polar:
        conc["winddirection"] = conc["winddirection"] / 180 * math.pi
        conc.drop(index=37, inplace=True) # this is value 990: variable winds
        conc.loc[0] = conc.loc[36].copy() # direction 0: no wind
        conc["winddirection"][0] = 0
        g = sns.FacetGrid(conc, subplot_kws=dict(projection='polar', theta_offset=math.pi/2, theta_direction=-1), height=10,
                          sharex=False, sharey=False, despine=False)
        g.map_dataframe(sns.histplot, x="windspeed", binwidth=math.pi/18, linewidth=4.0)
    else:
        lplot = (sns.histplot(data=conc, x="windspeed"))
        lplot.set(xlim=(5.0, 365.0))
    plt.show()
