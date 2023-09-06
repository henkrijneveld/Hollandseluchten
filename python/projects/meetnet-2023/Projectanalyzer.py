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

NL49704 = pd.DataFrame()
NL49551 = pd.DataFrame()
KNMI_225 = pd.DataFrame()
NL49557 = pd.DataFrame()
NL49701 = pd.DataFrame()
NL49573 = pd.DataFrame()
NL49561 = pd.DataFrame()
HLL_298 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
NL49553 = pd.DataFrame()
NL49572 = pd.DataFrame()
HLL_545 = pd.DataFrame()
NL49012 = pd.DataFrame()
NL49007 = pd.DataFrame()
HLL_420 = pd.DataFrame()
KNMI_209 = pd.DataFrame()
NL49570 = pd.DataFrame()
NL49017 = pd.DataFrame()
NL49014 = pd.DataFrame()
NL49703 = pd.DataFrame()
NL49556 = pd.DataFrame()
NL49016 = pd.DataFrame()
startdate = "20230101"
enddate = "20230901"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/meetnet-2023"


def removeFirstTwoRows(aDataframeList):
    for aFrame in aDataframeList:
        aFrame.drop(index=[aFrame.index[0], aFrame.index[1]], axis=0, inplace=True)

def plotPM25series(aFrame, title="PM25 data", knmiFrame=KNMI_240):
    lplot = sns.lineplot(aFrame, x="datetime", y="pm25")
    smootifyLineplot(lplot)
    lplot.set(title=title)
    plt.tight_layout()
    plt.show()

    wFrame = aFrame.copy()
    windPM_all = weatherFrame(wFrame, knmiFrame)
    windplot(windPM_all, "pm25", True, True, title=title+" winddirectiond", smooth=1)

def plotDiff25(leftFrame, rightFrame, title="difference", knmiFrame=KNMI_240):
    leftFrame = leftFrame.copy()
    rightFrame = rightFrame.copy()
    diff1 = diffFrame(leftFrame, rightFrame, "pm25")
    diff2 = diffFrame(rightFrame, leftFrame, "pm25")

    merged = pd.merge(diff1, diff2, on='datetime', suffixes=("_1", "_2"))
    merged["delta"] = merged.apply(lambda x: x["delta_pm25_1"] + x["delta_pm25_2"], axis=1)

#    diffs = diffFrame(diff1, diff2, "delta")

    lplot = sns.lineplot(merged, x="datetime", y="delta")
    smootifyLineplot(lplot)
    lplot.set(title=title)
    lplot.set(ylim=(-40,40))
    plt.tight_layout()
    plt.show()


    diff1 = weatherFrame(diff1, knmiFrame)
    windplot(diff1, "delta_pm25", True, True, title=title, smooth=0)

    diff2 = weatherFrame(diff2, knmiFrame)
    windplot(diff2, "delta_pm25", True, True, title=title, smooth=0)

def runit():
    # list of meetnet sensors to retrieve
    selectionwest = [NL49553, NL49557, NL49573, NL49570, NL49572, NL49551]
    selectionmiddle = [NL49561, NL49703, NL49704, NL49701, NL49556]
    selectioneast = [NL49007, NL49016, NL49012, NL49014, NL49017]
    selectionall = selectionwest + selectionmiddle + selectioneast

    removeFirstTwoRows(selectionall) # remove the fireworks peak at 1th januari

    setGlobalPlot()

    westdata = pd.concat(selectionwest)
    middledata = pd.concat(selectionmiddle)
    eastdata = pd.concat(selectioneast)

    loc_west = medianvalues([westdata], "datetime", "pm25")
    loc_middle = medianvalues([middledata], "datetime", "pm25")
    loc_east = medianvalues([eastdata], "datetime", "pm25")
    loc_all = medianvalues([westdata, middledata, eastdata], "datetime", "pm25")

    plotPM25series(NL49557, "West PM25 data 2023", KNMI_240)
#    plotPM25series(loc_west, "West PM25 data 2023", KNMI_240)

#    plotPM25series(loc_middle, "Middle PM25 data 2023", KNMI_240)
#    plotPM25series(loc_east, "East PM25 data 2023", KNMI_240)
#    plotPM25series(loc_all, "All PM25 data 2023", KNMI_240)

#    plotPM25series(NL49561, "Meetnetsensor 49561 (Schiphol next to knmi station)", KNMI_240)

#    plotPM25series(NL49573, "Meetnetsensor 49573 (West Beverwijk)", KNMI_225)
#    plotPM25series(NL49551, "Meetnetsensor 49551 (South Beverwijk)", KNMI_225)
#    plotPM25series(NL49572, "Meetnetsensor 49572 (East Beverwijk)", KNMI_225)
#    plotPM25series(NL49557, "Meetnetsensor 49557 (North Beverwijk)", KNMI_225)

#    plotDiff25(NL49573, NL49572, "East-West meetnet Beverwijk", KNMI_225)
#    plotDiff25(NL49551, NL49557, "North-South meetnet Beverwijk", KNMI_225)
#    plotDiff25(NL49016, NL49012, "West - East detectors Beverwijk", KNMI_240)
#    plotDiff25(NL49553, NL49557, "Top North detectors Beverwijk", KNMI_240)



#    diff = diffFrame(HLL_545, HLL_298, "pm25")
#    diff = weatherFrame(HLL_420)
#    windplot(diff, "delta", True, True)

#    lplot = sns.lineplot(loc_all, x="datetime", y="pm25")
#    smootifyLineplot(lplot)

#    diffPlot(NL49573, NL49572, "pm25")
    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



