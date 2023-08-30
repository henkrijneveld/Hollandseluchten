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

# show median of values in the winddirection of frame
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

# show number of count of every winddirection in fram
def windcountplot(frame, polar=True):
#    conc = frame.groupby("winddirection").count()
#    conc = conc.reset_index()
#    conc.columns.values[0] = "winddirection"
    conc = frame
    # drop variable winds
    conc.drop(conc[conc['winddirection'] == 990].index, inplace=True)
    # drop no wind
    conc.drop(conc[conc['winddirection'] == 0].index, inplace=True)
    if polar:
        conc.loc[conc["winddirection"] == 360, "winddirection"] = 0
        a = len(conc[conc["winddirection"] == 0])
        printf("Wind 0 = %d\n", a)
        b = len(conc[conc["winddirection"] == 360])
        printf("Wind 360 = %d\n", b)
        c = len(conc[conc["winddirection"] == 350])
        printf("Wind 350 = %d\n", c)
        d = len(conc[conc["winddirection"] == 340])
        printf("Wind 340 = %d\n", d)
        conc["winddirection"] = (conc["winddirection"] * math.pi) / 180.0
        g = sns.FacetGrid(conc, subplot_kws=dict(projection='polar', theta_offset=math.pi/2, theta_direction=-1), height=10,
                          sharex=False, sharey=False, despine=False)
        g.map_dataframe(sns.histplot, x="winddirection", binwidth=math.pi/18.01, linewidth=4.0)
    else:
        lplot = sns.histplot(data=conc, x="winddirection", binwidth=9.9999) # todo: wow just wow: 9.9999 instead of 10...
        lplot.set(xlim=(0.0, 380.0))
    plt.show()
