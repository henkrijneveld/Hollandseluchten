# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

import sys

import matplotlib.pyplot as plt

sys.path.insert(0, '../..')
from analyzer import *
from plotter import *
import math
import pprint as pp

KNMI_240 = pd.DataFrame()
KNMI_225 = pd.DataFrame()
startdate = "20200101"
enddate = "20230830"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/knmi-2020-2023"

def runit():
    setGlobalPlot()

#    windcountplot(KNMI_240, True, "Windcountplot Schiphol (240) from "+startdate+" to "+enddate)
#    windcountplot(KNMI_225, True, "Windcountplot ijmuiden (225) from "+startdate+" to "+enddate)

#    windplot(KNMI_240, "windspeed", title="Schiphol windspeed plot")
#    windplot(KNMI_225, "windspeed", title="IJmuiden windspeed plot")

#    merged = pd.merge(KNMI_240, KNMI_225, on="datetime", suffixes=("_Schiphol", "_IJmuiden"))
#    scatter = sns.scatterplot(merged, x="windspeed_Schiphol", y="windspeed_IJmuiden")
#    plt.show()

    merged = pd.merge(KNMI_240, KNMI_225, on="datetime", suffixes=("_Schiphol", "_IJmuiden"))
    scatter = sns.scatterplot(merged, x="winddirection_Schiphol", y="winddirection_IJmuiden")
    scatter.set(xlim=(5, 365))
    scatter.set(ylim=(5, 365))
    plt.show()


#    hplot = sns.histplot(data=KNMI_240, x="winddirection",binwidth=10)
#    hplot.set(xlim=(0, 370))
    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



