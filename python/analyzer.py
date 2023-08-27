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

def printf(template, *args):
    sys.stdout.write(template % args)

def create_var(var_name, var_value):
    globals()[var_name] = var_value

def convertToDatetime(aDate):
    dt = datetime.datetime(int(aDate[0:4]), int(aDate[4:6]), int(aDate[6:8]), 0, 0)
    dt = pd.Timestamp(dt)
    return dt.tz_localize("UTC")

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
    my_dpi = 96
    plt.figure(figsize=(1000 / my_dpi, 800 / my_dpi), dpi=my_dpi)

# make the relplots somewhat nicer when using datetime as x-axis
def smootifyRelplot(relplot):
    relplot.fig.subplots_adjust(bottom=0.1)
    for ax in relplot.axes:
        ax.tick_params(axis='x', labelrotation=30)
    plt.tight_layout()

def smootifyLineplot(lplot):
    lplot.tick_params(axis='x', labelrotation=30, bottom=True)
    plt.tight_layout()

