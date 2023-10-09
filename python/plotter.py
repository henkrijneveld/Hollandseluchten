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

sns.set(font_scale=1.75)
sns.set_style("whitegrid", {'grid.color': 'black',
                            'text.color': 'Blue',
                            'axes.labelcolor': 'blue'
})

myPalette = ["#FF0000", "#00FF00", "#0000FF"]
sns.set_palette(myPalette)

#@todo: wtf with figure sizes
my_dpi = 300
#plt.figure(figsize=(1000 / my_dpi, 800 / my_dpi), dpi=my_dpi)

def describePlot(aFrame, aTitle):
    print("Describe: " + aTitle)
    print(aFrame.describe())
    print("---")


def setPlotSizeSquare():
    global my_dpi
    plt.figure(figsize=(2000 / my_dpi, 2000 / my_dpi), dpi=my_dpi)

def setPlotSizeLandscape():
    global my_dpi
    plt.figure(figsize=(2000 / my_dpi, 1600 / my_dpi), dpi=my_dpi)

def simpleScatterPlot(aDataFrame, x, y,  xlim=(-40.0, 40.0), ylim=(-40.0, 40.0), title="Scatterplot", filename=False,
                      describe=False):
    # same length on x and y, assume square, otherwise landscape
    if (xlim[1]-xlim[0]) == (ylim[1]-ylim[0]):
        setPlotSizeSquare()
    else:
        setPlotSizeLandscape()

    scatter = sns.scatterplot(aDataFrame, x=x, y=y)
#    scatter = sns.jointplot(aDataFrame, x=x, y=y)

    scatter.set(title=title)
    scatter.set(xlim=xlim)
    scatter.set(ylim=ylim)
    plt.tight_layout()
    plt.show()
    if describe:
        print("Describe: " + title)
        print(aDataFrame[y].describe())
        print("---")
    if filename:
        scatter.get_figure().savefig(filename)

def simpleJointPlot(aDataFrame, x, y,  xlim=(-40.0, 40.0), ylim=(-40.0, 40.0), title="Scatterplot", filename=False,
                      describe=False):
    # same length on x and y, assume square, otherwise landscape
    if (xlim[1]-xlim[0]) == (ylim[1]-ylim[0]):
        setPlotSizeSquare()
    else:
        setPlotSizeLandscape()

    scatter = sns.jointplot(aDataFrame, x=x, y=y,
                            xlim=xlim, ylim=ylim)
    plt.tight_layout()
    plt.show()
    if describe:
        print("Describe: " + title)
        print(aDataFrame[y].describe())
        print("---")
    if filename:
        scatter.get_figure().savefig(filename)


def simpleStripPlot(aDataFrame, x, y,  xlim=(-40.0, 40.0), ylim=(-40.0, 40.0), title="Scatterplot", filename=False,
                      describe=False):
    # same length on x and y, assume square, otherwise landscape
    if (xlim[1]-xlim[0]) == (ylim[1]-ylim[0]):
        setPlotSizeSquare()
    else:
        setPlotSizeLandscape()

    scatter = sns.stripplot(aDataFrame, x=x, y=y, size=1, jitter=0.2)

    scatter.set(title=title)
    scatter.set(xlim=xlim)
    scatter.set(ylim=ylim)
    plt.tight_layout()
    plt.show()
    if describe:
        print("Describe: " + title)
        print(aDataFrame[y].describe())
        print("---")
    if filename:
        scatter.get_figure().savefig(filename)

def printSeries(aSensor, title="PM Series", filename=False, ylim=None):
    lplot = sns.lineplot(aSensor, x="datetime", y="pm25")
    lplot.set(title=title)
    if ylim:
        lplot.set(ylim=ylim)
    lplot.tick_params(axis='x', labelrotation=30, bottom=True)
    plt.tight_layout()
    plt.show()
    if filename:
        lplot.get_figure().savefig(filename)

def printSeries_on_ax(aSensor, title="PM Series", filename=False, ylim=None, ax=None):
    ax.set(title=title)
    ax.tick_params(axis='x', which="both", labelrotation=30, bottom=True)
    lplot = sns.lineplot(aSensor, x="datetime", y="pm25", ax=ax)
    if ylim:
        lplot.set(ylim=ylim)
    if filename:
        lplot.get_figure().savefig(filename)

# histogram attributeplot on attribute name
def attrPlot(aDataFrame, attr, xlim=(-40.0, 40.0), title="Difference", filename=False, binwidth=0.10, describe=False):
    setPlotSizeLandscape()
    lplot = sns.histplot(data=aDataFrame, x=attr, binwidth=binwidth, kde=True)
    lplot.set(xlim=xlim)
    lplot.set(title=title)
    plt.tight_layout()
    plt.show()
    if describe:
        describePlot(aDataFrame[attr], title)
    if filename:
        lplot.get_figure().savefig(filename)

    return

# difplot on attribute name
def diffPlot(leftframe, rightframe, attr, xlim=(-40.0, 40.0), title="Difference", filename=False,
             describe=False):
    deltas = analyzer.diffFrame(leftframe, rightframe, attr)
    lplot = sns.histplot(data=deltas, x="delta_"+attr, binwidth=0.1, kde=False)
    lplot.set(xlim=xlim)
    lplot.set(title=title)
    plt.tight_layout()
    plt.show()
    if describe:
        describePlot(deltas["delta_"+attr], title)
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
    plt.tight_layout()
    plt.show()
    if filename:
        lplot.get_figure().savefig(filename)
    return

# fill missing wind directions and remove 0 and 990
def fillmissingwinddirections(aFrame):
    directions = range(10, 370, 10)
    target = pd.DataFrame(directions, columns=['winddirection'])
    target = pd.merge(target, aFrame, on="winddirection", how="inner") # make sure everything from 10 - 260 is there
    target.at[35, "winddirection"] = 0
    target.sort_values(by=["winddirection"], inplace=True)
    target.reset_index(inplace=True, drop=True)
    target.loc[36] = target.loc[0].copy()  # make the circle round
    target.at[36, "winddirection"] = 360
    return target

# show median of values in the winddirection of frame, value in steps + and - 10 degrees
def windplot(frame, values, polar=True, useMedian=True, title="Windplot", smooth=1, method="medianvalues", filename=False):
    global functions
    conc = frame.copy()
    if not useMedian:
        values = values + "_mean"
#   conc = medianvalues([conc], "winddirection", values)
    conc = getattr(analyzer, method)([conc], "winddirection", values)
    conc = fillmissingwinddirections(conc)

    if smooth:
        # dirty
        svalues = values + "_avg_" + str(smooth * 20) + "°"
        conc = conc.assign(newcolumn=0)
        conc = conc.rename(columns={"newcolumn": svalues})
        conc = conc.astype({svalues: 'float64'})
        for i in range(0,37):
            for j in range(-smooth, smooth+1):
                conc.at[i, svalues] += conc[values][(i+j) % 36]
            conc.at[i, svalues] /= smooth * 2 + 1
        values = svalues

    if polar:
        conc["winddirection"] = conc["winddirection"] / 180 * math.pi
        conc["winddirection"][0] = 0

        g = sns.FacetGrid(conc, subplot_kws=dict(projection='polar', theta_offset=math.pi/2,
                          theta_direction=-1), height=6.4, sharex=False, sharey=False,
                          despine=False)
        g.fig.suptitle(title, fontsize=17)
        g.map_dataframe(sns.lineplot, x="winddirection", y=values, linewidth=4.0)
        g.set(xlabel=None)
        g.set(ylabel=None)

        plt.tight_layout()

        if filename:
            g.savefig(filename)

    else:
        lplot = (sns.lineplot(data=conc, x="winddirection", y=values, linewidth=2.5))
        lplot.set(xlim=(-5.0, 365.0))
        lplot.set(title=title)
        lplot.set_ylabel(values.replace("_", " "), fontsize=14)
        lplot.set_xlabel("winddirection", fontsize=14)
        lplot.axes.set_title(title, fontsize=17)

        plt.tight_layout()

        if filename:
            lplot.get_figure().savefig(filename)

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
