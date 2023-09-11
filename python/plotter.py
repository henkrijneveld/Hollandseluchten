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

import analyzer

def printSeries(aSensor, title="PM Series", filename=False):
    lplot = sns.lineplot(aSensor, x="datetime", y="pm25")
    lplot.set(title=title)
    lplot.tick_params(axis='x', labelrotation=30, bottom=True)
    plt.tight_layout()
    plt.show()
    if filename:
        lplot.get_figure().savefig(filename)

# difplot on attribute name
def diffPlot(leftframe, rightframe, attr, xlim=(-40.0, 40.0), title="Difference", filename=False):
    deltas = analyzer.diffFrame(leftframe, rightframe, attr)
    lplot = sns.histplot(data=deltas, x="delta_"+attr, binwidth=0.10, kde=True)
    lplot.set(xlim=xlim)
    lplot.set(title=title)
    plt.show()
    if filename:
        lplot.get_figure().savefig(filename)

    return

# relative difplot on attribute name
def diffPlotRelative(leftframe, rightframe, attr, xlim=(-3.0, 3.0), title="Difference", filename=False):
    deltas = analyzer.relativeFrame(leftframe, rightframe, attr)
    lplot = sns.histplot(data=deltas, x="delta_"+attr, binwidth=0.10, kde=True)
    lplot.set(xlim=xlim)
    lplot.set(title=title)
    plt.show()
    if filename:
        lplot.get_figure().savefig(filename)

    return


def diffWindPlot(leftframe, rightframe, xlim=(-170.0, 170.0), title="Winddifference", filename=False):
    deltas = analyzer.diffWindFrame(leftframe, rightframe)
    deltas["delta_winddirection"] = (deltas["delta_winddirection"] - 5)  # shift to middle for histogram
    lplot = sns.histplot(data=deltas, x="delta_winddirection", binwidth=10, kde=False)
    lplot.set(title=title)
    lplot.set(xlim=xlim)
    plt.show()
    if filename:
        lplot.get_figure().savefig(filename)
    return

# show median of values in the winddirection of frame, value in steps + and - 10 degrees
def windplot(frame, values, polar=True, useMedian=True, title="Windplot", smooth=1, method="medianvalues", filename=False):
    global functions
    conc = frame.copy()
#   conc = medianvalues([conc], "winddirection", values)
    conc = getattr(analyzer, method)([conc], "winddirection", values)

    if not useMedian:
        values = values + "_mean"
    if polar:
        conc["winddirection"] = conc["winddirection"] / 180 * math.pi
        if 37 in conc.index:
            conc.drop(index=37, inplace=True) # this is value 990: variable winds
        conc.loc[0] = conc.loc[36].copy() # direction 0: no wind
        conc["winddirection"][0] = 0
        if smooth:
            # dirty
            svalues = values + "_smooth"
            conc = conc.assign(newcolumn=0)
            conc = conc.rename(columns={"newcolumn": svalues})
            conc = conc.astype({svalues: 'float64'})
            for i in range(0,37):
                for j in range(-smooth, smooth+1):
                    conc.at[i, svalues] += conc[values][(i+j) % 36]
                conc.at[i, svalues] /= smooth * 2 + 1
            values = svalues

        g = sns.FacetGrid(conc, subplot_kws=dict(projection='polar', theta_offset=math.pi/2,
                          theta_direction=-1), height=10, sharex=False, sharey=False,
                          despine=False)
        g.fig.suptitle(title)
        g.map_dataframe(sns.lineplot, x="winddirection", y=values, linewidth=4.0)
        if filename:
            g.savefig(filename)

    else:
        lplot = (sns.scatterplot(data=conc, x="winddirection", y=values))
        lplot.set(xlim=(5.0, 365.0))
        if filename:
            lplot.get_figure().savefig(filename)

    plt.tight_layout()
    plt.show()

# show number of count of every winddirection in frame
def windcountplot(frame, polar=True, title="wind count plot"):
#    conc = frame.groupby("winddirection").count()
#    conc = conc.reset_index()
#    conc.columns.values[0] = "winddirection"
    conc = frame.copy()
    # drop variable winds
    conc.drop(conc[conc['winddirection'] == 990].index, inplace=True)
    # drop no wind
    conc.drop(conc[conc['winddirection'] == 0].index, inplace=True)
    if polar:
        conc.loc[conc["winddirection"] == 360, "winddirection"] = 0

        conc["winddirection"] = (conc["winddirection"] * math.pi) / 180.0 - math.pi/36 # shift to middle
        g = sns.FacetGrid(conc, subplot_kws=dict(projection='polar', theta_offset=math.pi/2, theta_direction=-1), height=10,
                          sharex=False, sharey=False, despine=False)
        g.fig.suptitle(title)
        g.map_dataframe(sns.histplot, x="winddirection", binwidth=math.pi/18.001, linewidth=4.0)
    else:
        lplot = sns.histplot(data=conc, x="winddirection", binwidth=9.9999)
        lplot.set(xlim=(0.0, 380.0))
    plt.tight_layout()
    plt.show()
