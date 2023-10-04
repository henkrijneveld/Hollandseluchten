# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime
import seaborn as sns
import sys
import os
import pprint as pp
from plotter import *

def printf(template, *args):
    sys.stdout.write(template % args)

def create_var(var_name, var_value):
    globals()[var_name] = var_value

def convertToDatetime(aDate):
    dt = datetime.datetime(int(aDate[0:4]), int(aDate[4:6]), int(aDate[6:8]), 0, 0)
    dt = pd.Timestamp(dt)
    return dt.tz_localize("UTC")

def dropNoWindDirection(aFrame):
    # drop variable winds
    aFrame.drop(aFrame[aFrame['winddirection'] == 990].index, inplace=True)
    # drop no wind
    aFrame.drop(aFrame[aFrame['winddirection'] == 0].index, inplace=True)

def printGlobals(projectdir):
    prefix = ""
    startdate = False
    enddate = False
    for file in os.listdir(projectdir):
        if file.endswith(".csv"):
            tmpFrame = pd.read_csv(projectdir + "/" + file)
            tmpFrame["datetime"] = pd.to_datetime(tmpFrame["datetime"])
            tmpFrame["datetime"] = tmpFrame["datetime"].dt.tz_localize(None)
            fname = file[:-4]
            printf("%s%s = pd.DataFrame()\n", prefix, fname)
            if (not startdate):
                startdate = tmpFrame["datetime"].min()
            if (not enddate):
               enddate = tmpFrame["datetime"].min()
            if tmpFrame["datetime"].min() < startdate:
                startdate = tmpFrame["datetime"].min()
            if tmpFrame["datetime"].max() > enddate:
                enddate = tmpFrame["datetime"].max()
            start = startdate.strftime("%Y%m%d")
            end = enddate.strftime("%Y%m%d")
    printf('startdate = "%s"\n', start)
    printf('enddate = "%s"\n', end)
    printf('projectdir = "%s"\n', projectdir)
    printf("\nDone reading filenames\n")
    exit(0)

def importDataframes(projectdir, globalcontext):
    printf("Importing: ")
    for file in os.listdir(projectdir):
        if file.endswith(".csv"):
            tmpFrame = pd.read_csv(projectdir + "/" + file)
            tmpFrame["datetime"] = pd.to_datetime(tmpFrame["datetime"])
            tmpFrame = removeDatesBefore(tmpFrame, "2023-01-01 04:00:00+00:00")
            fname = file[:-4]
            if not fname in globalcontext:
                printf("File %s added to globals\n", fname)
            tmpFrame["sensorname"] = fname
            globalcontext[fname] = tmpFrame

    printf("\nDone importing\n")

# palette examples: https://seaborn.pydata.org/tutorial/color_palettes.html
def setGlobalPlot():
    sns.set_theme(style="whitegrid")
    sns.set_context("notebook")
#    pp.pprint(sns.axes_style())
#    pp.pprint(sns.plotting_context())
    sns.set_palette("muted")
    my_dpi = 300
    plt.figure(figsize=(2000 / my_dpi, 1600 / my_dpi), dpi=my_dpi)

# make the relplots somewhat nicer when using datetime as x-axis
def smootifyRelplot(relplot):
    relplot.fig.subplots_adjust(bottom=0.1)
    for ax in relplot.axes:
        ax.tick_params(axis='x', labelrotation=30)
    plt.tight_layout()

def smootifyLineplot(lplot):
    lplot.tick_params(axis='x', labelrotation=30, bottom=True)
    plt.tight_layout()

# the framelist values are concatenated, and the median and mean values are determined on the groupby attribute
# a dataframe with a single row for every groupby value is returned
def medianvalues(framelist, groupby, value):
    totalframe = pd.concat(framelist).copy()
    totalframe.sort_values(groupby, inplace=True)
    result = totalframe.groupby(groupby)[value].median().to_frame()
    result = result.reset_index()
    result.columns.values[0] = groupby
    result.columns.values[1] = value
    result[value+"_mean"] = totalframe.groupby(groupby)[value].mean().values
    return result

# the framelist values are concatenated, and the median and mean values are determined on the groupby attribute
# a dataframe with a single row for every groupby value is returned
def meanvalues(framelist, groupby, value):
    totalframe = pd.concat(framelist)
    totalframe.sort_values(groupby, inplace=True)
    result = totalframe.groupby(groupby)[value].mean().to_frame()
    result = result.reset_index()
    result.columns.values[0] = groupby
    result.columns.values[1] = value
    return result

# the framelist values are concatenated, and the median and mean values are determined on the groupby attribute
# a dataframe with a single row for every groupby value is returned
def maxvalues(framelist, groupby, value):
    totalframe = pd.concat(framelist)
    totalframe.sort_values(groupby, inplace=True)
    result = totalframe.groupby(groupby)[value].max().to_frame()
    result = result.reset_index()
    result.columns.values[0] = groupby
    result.columns.values[1] = value
    return result

# the framelist values are concatenated, and the median and mean values are determined on the groupby attribute
# a dataframe with a single row for every groupby value is returned
def minvalues(framelist, groupby, value):
    totalframe = pd.concat(framelist)
    totalframe.sort_values(groupby, inplace=True)
    result = totalframe.groupby(groupby)[value].min().to_frame()
    result = result.reset_index()
    result.columns.values[0] = groupby
    result.columns.values[1] = value
    return result


# the count of groupby values
# returns groupby values and counts
def countvalues(aFrame, groupby):
    totalframe = aFrame.copy()
    totalframe.sort_values(groupby, inplace=True)
    totalframe = totalframe.assign(count=0)
    result = totalframe.groupby(groupby)["count"].count().to_frame()
    result = result.reset_index()
    result.columns.values[0] = groupby
    result["count"] = totalframe.groupby(groupby)[groupby].count().values
    return result


# The difference of attr for the left- and right frames is returned
# based on datetime. Resulting value is "delta_" + attr
def diffFrame(leftframe, rightframe, attr):
    merged = pd.merge(leftframe, rightframe, on='datetime', suffixes=("_left", "_right"))
    merged["delta"] = merged.apply(lambda x: x[attr+"_left"] - x[attr+"_right"], axis=1)
    deltas = pd.DataFrame()
    deltas["delta_"+attr] = merged["delta"].copy()
    deltas["datetime"] = merged["datetime"].copy()
    deltas.sort_values(inplace=True, ignore_index=True, by="delta_"+attr)
    return deltas


def relative(aRow):
    left = aRow["pm25_left"]
    right = aRow["pm25_right"]
    if left < 0.1:
        return 99
    if right < 0.1:
        return 89
    reldiff = 1 - (left - right) / left
    return reldiff

# The relative difference of attr for the left- and right frames is returned
# based on datetime. Resulting value is "delta_" + attr
# difference == 1 means they are the same
def relativeFrame(leftframe, rightframe, attr):
    merged = pd.merge(leftframe, rightframe, on='datetime', suffixes=("_left", "_right"))
    merged["delta"] = merged.apply(relative, axis=1)
    deltas = pd.DataFrame()
    deltas["delta_"+attr] = merged["delta"].copy()
    deltas["datetime"] = merged["datetime"].copy()
    deltas.sort_values(inplace=True, ignore_index=True, by="delta_"+attr)
    print(deltas.describe())
    return deltas


# compute winddiffeerence
def winddif(aRow):
    srcwind = aRow["winddirection_left"]
    compwind = aRow["winddirection_right"]
    diff = compwind - srcwind
    if diff < -170:
        diff = 360 + diff
    if diff > 180:
        diff = diff - 360
    return diff

# The difference on wuinddirection for the left- and right frames is returned
# for winddirection values.
# if any value is 0 or 990 it is ignored
# based on datetime. Resulting value is "delta_" + attr
def diffWindFrame(leftframe, rightframe):
    merged = pd.merge(leftframe, rightframe, on='datetime', suffixes=("_left", "_right"))
    merged["delta"] = merged.apply(winddif, axis=1)
    deltas = pd.DataFrame()
    deltas["delta_winddirection"] = merged["delta"].copy()
    deltas["datetime"] = merged["datetime"].copy()
    deltas.sort_values(inplace=True, ignore_index=True, by="delta_winddirection")
#    print(deltas.describe())
    return deltas

# merge knmi-2020-2023 data into a frame on key datetime
def weatherFrame(aFrame, knmiFrame = "KNMI_240"):
    conc = pd.merge(aFrame, knmiFrame, on="datetime", suffixes=("", "_knmi"))
    conc = conc.rename({'windspeed_knmi': 'windspeed', 'winddirection_knmi': 'winddirection'}, axis=1)
    return conc


def removeDatesBefore(aDataframe, aDate="2023-01-01 21:00:00+00:00"):
    return aDataframe[aDataframe["datetime"] > pd.to_datetime(aDate)].copy()

def removeDatesAfter(aDataframe, aDate="2023-01-01 21:00:00+00:00"):
    return aDataframe[aDataframe["datetime"] < pd.to_datetime(aDate)].copy()


def plotPM25series(aFrame, showLineplot=False, title="PM25 data", knmiFrame=None, method="medianvalues", filename=False):
    if showLineplot:
        lplot = sns.lineplot(aFrame, x="datetime", y="pm25")
        smootifyLineplot(lplot)
        lplot.set(title=title)
        plt.tight_layout()
        plt.show()

    wFrame = aFrame.copy()
    windPM_all = weatherFrame(wFrame, knmiFrame)
    windplot(windPM_all, "pm25", True, True, title=title+" winddirectiond",
             smooth=1, method=method, filename=filename)

def plotDiff25(leftFrame, rightFrame, title="difference", knmiFrame=None, filename=False, smooth=1):
    leftFrame = leftFrame.copy()
    rightFrame = rightFrame.copy()
    diff1 = diffFrame(leftFrame, rightFrame, "pm25")
#    diff2 = diffFrame(rightFrame, leftFrame, "pm25")

#    merged = pd.merge(diff1, diff2, on='datetime', suffixes=("_1", "_2"))
#    merged["delta"] = merged.apply(lambda x: x["delta_pm25_1"] + x["delta_pm25_2"], axis=1)

#    diffs = diffFrame(diff1, diff2, "delta")

#    lplot = sns.lineplot(merged, x="datetime", y="delta")
#    smootifyLineplot(lplot)
#    lplot.set(title=title)
#    lplot.set(ylim=(-40,40))
#    plt.tight_layout()
#    plt.show()

    diff1 = weatherFrame(diff1, knmiFrame)
    windplot(diff1, "delta_pm25", True, True, title=title, smooth=smooth, filename=filename)

#    diff2 = weatherFrame(diff2, knmiFrame)
#    windplot(diff2, "delta_pm25", True, True, title=title, smooth=0)

def createTimeSeries(aCollection, projectdir, namesuffix=""):
    for sensortuple in aCollection:
        sensordata, sensor = sensortuple
        printSeries(sensordata, sensor + " " + namesuffix, projectdir + "/timeseries-" + sensor + "-" + namesuffix,
                    ylim=(-20,50))

def createTimeSeries_Multiple(aCollection, projectdir, namesuffix=""):
    total = len(aCollection)
    nrcols = min(total, 3)
    nrrows = math.ceil(total / 3)
    fig, axes = plt.subplots(nrrows, nrcols, figsize=(20,20), sharey=True, sharex=True)
    for lastcomn in range(0, nrcols):
        axes[nrrows - 1, lastcomn].tick_params(axis='x', which="both", labelrotation=30, bottom=True)
    colnr = 0
    rownr = 0
    for sensortuple in aCollection:
        sensordata, sensor = sensortuple
        printSeries_on_ax(sensordata, sensor + " " + namesuffix, projectdir + "/timeseries-" + sensor + "-" + namesuffix,
                    ylim=(-20,50), ax=axes[rownr, colnr])
        colnr += 1
        if colnr > 2:
            colnr = 0
            rownr += 1

    plt.tight_layout()
    plt.show()

