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

# General
superFrame = pd.DataFrame()
superFrameAugmented = pd.DataFrame()
HLL_452 = pd.DataFrame()  # East
HLL_226 = pd.DataFrame()  # North
HLL_433 = pd.DataFrame()  # West
HLL_513 = pd.DataFrame()  # South

NLMedian = pd.DataFrame()
NL49570 = pd.DataFrame()
NL49557 = pd.DataFrame()
KNMI_225 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
NL49553 = pd.DataFrame()
NL49572 = pd.DataFrame()
NL49573 = pd.DataFrame()
NL49551 = pd.DataFrame()
startdate = "20230101"
enddate = "20230901"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/Industrie-Ijmuiden"

def createTimeSeries(aCollection, namesuffix=""):
    for sensor in aCollection:
        sensordata = globals()[sensor]
        printSeries(sensordata, sensor + " " + namesuffix, projectdir + "/timeseries-" + sensor + "-" + namesuffix,
                    ylim=(-20,50))

def createTimeSeries_Multiple(aCollection, namesuffix=""):
    total = len(aCollection)
    nrcols = min(total, 3)
    nrrows = math.ceil(total / 3)
    fig, axes = plt.subplots(nrrows, nrcols, figsize=(20,20), sharey=True, sharex=True)
    for lastcomn in range(0, nrcols):
        axes[nrrows - 1, lastcomn].tick_params(axis='x', which="both", labelrotation=30, bottom=True)
    colnr = 0
    rownr = 0
    for sensor in aCollection:
        sensordata = globals()[sensor]
        printSeries_on_ax(sensordata, sensor + " " + namesuffix, projectdir + "/timeseries-" + sensor + "-" + namesuffix,
                    ylim=(-20,50), ax=axes[rownr, colnr])
        colnr += 1
        if colnr > 2:
            colnr = 0
            rownr += 1

    plt.tight_layout()
    plt.show()


# return a dataframe with all relevant data
#  datetime
#  pm25 virtual median value
#  pm25-<sensornr>
#  knmidata
#
# write to csv when done
#
# Will be autoloaded next time script is run, so no need to call this function
# everytime.
def createSuperFrame(sensors, knmi):
    global superFrame
    merged = pd.DataFrame()

    for sensor in sensors:
        sensorFrame = globals()[sensor]
        if merged.empty:
            merged = sensorFrame.copy()
        else:
            merged = pd.merge(merged, sensorFrame, on='datetime',
                              suffixes=("", "_" + sensor))
            merged.drop(['sensorname'+'_'+sensor], axis=1, inplace=True)
    merged.drop(['sensorname'], axis=1, inplace=True)
    # delete 0 and 990
    knmi = knmi[(knmi["winddirection"] < 369) & (knmi["winddirection"] > 5)]
    merged = pd.merge(merged, knmi, on='datetime',
                      suffixes=("", "_knmi"))
    merged.drop(['sensorname'], axis=1, inplace=True)
    merged.drop(merged.columns[0], axis=1, inplace=True)

    superFrame = merged.copy()
#    superFrame.to_csv(projectdir + "/superFrame.csv", index=False)

    return merged

def diff_N557_SHLL513(aRow):
    north = aRow["pm25_NL49557"]
    #north = aRow["pm25_NL49553"]
    south = aRow["pm25_HLL_513"]
    return north - south

def diff_NHLL226_S551(aRow):
    north = aRow["pm25_HLL_226"]
    #north = aRow["pm25_NL49553"]
    south = aRow["pm25_NL49551"]
    return north - south

def diff_NHLL226_SHLL513(aRow):
    north = aRow["pm25_HLL_226"]
    south = aRow["pm25_HLL_513"]
    return north - south

def diff_W573_EHLL452(aRow):
    west = aRow["pm25_NL49573"]
    east = aRow["pm25_HLL_452"]
    return west - east

def diff_WHLL433_E572(aRow):
    west = aRow["pm25_HLL_433"]
    east = aRow["pm25_NL49572"]
    return west - east

def diffWE(aRow):
    west = aRow["pm25_NL49573"]
    east = aRow["pm25_NL49572"]
    return west - east


def diffNS(aRow):
    north = aRow["pm25_NL49557"]
    #north = aRow["pm25_NL49553"]
    south = aRow["pm25_NL49551"]
    return north - south

def diffNS553(aRow):
#    north = aRow["pm25_NL49557"]
    north = aRow["pm25_NL49553"]
    south = aRow["pm25_NL49551"]
    return north - south

def diffcoloc(aRow):
    ref = aRow["pm25_NL49557"]
    coloc = aRow["pm25_NL49553"]
    return ref - coloc

def pm25Upwind(aRow):
    wind = aRow["winddirection"]
    pm25 = 0
    if wind > 45 and wind < 135:
        pm25 = aRow["pm25_NL49572"]
    if wind > 135 and wind < 225:
        pm25 = aRow["pm25_NL49551"]
    if wind > 225 and wind < 315:
        pm25 = aRow["pm25_NL49573"]
    if wind > 315 or wind < 45:
        pm25 = aRow["pm25_NL49557"]
        #pm25 = aRow["pm25_NL49553"]
    return pm25

def pm25Downwind(aRow):
    wind = aRow["winddirection"]
    pm25 = 0
    if wind > 45 and wind < 135:
        pm25 = aRow["pm25_NL49573"]
    if wind > 135 and wind < 225:
        pm25 = aRow["pm25_NL49557"]
        #pm25 = aRow["pm25_NL49553"]
    if wind > 225 and wind < 315:
        pm25 = aRow["pm25_NL49572"]
    if wind > 315 or wind < 45:
        pm25 = aRow["pm25_NL49551"]
    return pm25

def pm25diff(aRow):
    wind = aRow["winddirection"]
    downwind = aRow["pm25_downwind"]
    upwind = aRow["pm25_upwind"]
    return downwind - upwind

# add columns:
#   pm25_diff_WE
#   pm25_diff_NS
#   pm25_diff_coloc (diff to NL49553 - NL49557)
#   pm25_upwind (pm25 without the local source)
#   pm25_diff_winddirection (pm25 difference in winddirection)
#
# write result to superFrameAugmented.csv
def augmentSuperframe():
    global superFrameAugmented

    superFrame["pm25_diff_N557_SHLL513"] = superFrame.apply(diff_N557_SHLL513, axis=1)
    superFrame["pm25_diff_NHLL226_S551"] = superFrame.apply(diff_NHLL226_S551, axis=1)
    superFrame["pm25_diff_W573_EHLL452"] = superFrame.apply(diff_W573_EHLL452, axis=1)
#    superFrame["pm25_diff_WHLL433_E572"] = superFrame.apply(diff_WHLL433_E572, axis=1)
    superFrame["pm25_diff_NHLL226_SHLL513"] = superFrame.apply(diff_NHLL226_SHLL513, axis=1)


    superFrame["pm25_diff_WE"] = superFrame.apply(diffWE, axis=1)
    superFrame["pm25_diff_NS"] = superFrame.apply(diffNS, axis=1)
    superFrame["pm25_diff_NS_553"] = superFrame.apply(diffNS553, axis=1)
    superFrame["pm25_diff_coloc"] = superFrame.apply(diffcoloc, axis=1)
    superFrame["pm25_upwind"] = superFrame.apply(pm25Upwind, axis=1)
    superFrame["pm25_downwind"] = superFrame.apply(pm25Downwind, axis=1)
    superFrame["pm25_diff_winddirection"] = superFrame.apply(pm25diff, axis=1)

    superFrameAugmented = superFrame.copy()
    #superFrameAugmented.to_csv(projectdir + "/superFrameAugmented.csv", index=False)

    return superFrameAugmented


def runit():
    global NLMedian
    global superFrameAugmented
    global HLL_433

#    HLL_433 =  removeDatesBefore(HLL_433, aDate="2023-04-01 00:00:00+00:00")

    allSensors = ["NLMedian", "NL49570", "NL49557", "NL49553", "NL49572", "NL49573", "NL49551"]
    allHLLSensors = ["HLL_513", "HLL_226", "HLL_452"]

    # replace NLMedian  with valuse from Velsen Noord
    NLMedian = medianvalues([NL49570, NL49557, NL49553, NL49572, NL49573, NL49551],
                            "datetime", "pm25")
    NLMedian["sensorname"] = "NLMedian"

#    createTimeSeries(allSensors, namesuffix="pm25")
#    createTimeSeries(allHLLSensors, namesuffix="pm25")
#    createTimeSeries_Multiple(allSensors, namesuffix="pm25")

#@todo these functions generate the intersection of the frames. As 433 has two
    # months without data, these months are now ignored
    createSuperFrame(allSensors + allHLLSensors, KNMI_225)
    augmentSuperframe()

    windplot(superFrameAugmented, "pm25_diff_NS", polar=False,
             useMedian=True, title="PM25 difference N-S", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotNS")

    windplot(superFrameAugmented, "pm25_diff_NS_553", polar=False,
             useMedian=True, title="PM25 difference N-S 553", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotNS_553")
    windplot(superFrameAugmented, "pm25_diff_NS", polar=False,
             useMedian=True, title="PM25 difference N-S", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotNS")

    windplot(superFrameAugmented, "pm25_diff_NHLL226_SHLL513", polar=False,
             useMedian=True, title="PM25 difference N (HLL) - S (HLL)", smooth=3,
             method="medianvalues", filename=projectdir + "/windplotNS_NHLL226_SHLL513")
    return

    printSeries(HLL_433, "HLL_433 pm25", projectdir + "/timeseries-" + "HLL_433-pm25",
                ylim=(-20, 150))
    printSeries(HLL_513, "HLL_513 pm25", projectdir + "/timeseries-" + "HLL_433-pm25",
                ylim=(-20, 150))

    diffPlot(HLL_226, NL49557, "pm25", xlim=(-25.0, 25.0), title="Difference HLL 226 vs Meetnet 557 ",
             filename = projectdir + "/diffplot_HLL_226_Meetnet_557")
    diffPlot(HLL_226, HLL_513, "pm25", xlim=(-20.0, 20.0), title="Difference HLL 226 vs HLL 513 ",
             filename=projectdir + "/diffplot_HLL_226_HLL_513")
    diffPlot(HLL_513, NL49551, "pm25", xlim=(-25.0, 25.0), title="Difference HLL 513 vs Meetnet 551 ",
             filename = projectdir + "/diffplot_HLL_513_Meetnet_551")
    diffPlot(NL49557, NL49551, "pm25", xlim=(-25.0, 25.0), title="Difference Meetnet 557 vs Meetnet 551 ",
             filename = projectdir + "/diffplot_Meetnet_557_Meetnet_551")
    diffPlot(NL49553, NL49551, "pm25", xlim=(-25.0, 25.0), title="Difference Meetnet 553 vs Meetnet 551 ",
             filename = projectdir + "/diffplot_Meetnet_553_Meetnet_551")
    diffPlot(NL49553, NL49557, "pm25", xlim=(-25.0, 25.0), title="Difference Meetnet 553 vs Meetnet 557 ",
             filename = projectdir + "/diffplot_Meetnet_553_Meetnet_557")

    windplot(superFrameAugmented, "pm25_diff_N557_SHLL513", polar=False,
             useMedian=True, title="PM25 difference N (meetnet) - S (HLL)", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotNS_N557_SHLL513")

    windplot(superFrameAugmented, "pm25_diff_NHLL226_S551", polar=False,
             useMedian=True, title="PM25 difference N (HLL) - S (meetnet)", smooth=3,
             method="medianvalues", filename=projectdir + "/windplotNS_NHLL226_S551")

    windplot(superFrameAugmented, "pm25_diff_NHLL226_SHLL513", polar=False,
             useMedian=True, title="PM25 difference N (HLL) - S (HLL)", smooth=3,
             method="medianvalues", filename=projectdir + "/windplotNS_NHLL226_SHLL513")

    windplot(superFrameAugmented, "pm25_diff_W573_EHLL452", polar=False,
             useMedian=True, title="PM25 difference W (meetnet) - E (HLL)", smooth=3,
             method="medianvalues", filename=projectdir + "/windplotWE_W573_EHLL452")

    windplot(superFrameAugmented, "pm25_diff_WHLL433_E572", polar=False,
         useMedian=True, title="PM25 difference W (HLL) - E (meetnet)", smooth=3,
         method="medianvalues", filename=projectdir + "/windplotWE_WHLL433_E572")

    windplot(superFrameAugmented, "pm25_diff_NS_553", polar=False,
             useMedian=True, title="PM25 difference N-S 553", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotNS_553")
    windplot(superFrameAugmented, "pm25_diff_NS", polar=False,
             useMedian=True, title="PM25 difference N-S", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotNS")

    windplot(superFrameAugmented, "pm25_diff_WE", polar=False,
             useMedian=True, title="PM25 difference W-E", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotWE")
    windplot(superFrameAugmented, "pm25_diff_coloc", polar=True,
             useMedian=True, title="PM25 difference colocation", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotcoloc")
    windplot(superFrameAugmented, "pm25_upwind", polar=True,
             useMedian=True, title="PM25 upwind concentration", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotUpwind")
    windplot(superFrameAugmented, "pm25_downwind", polar=True,
             useMedian=True, title="PM25 downwind concentration", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotDownwind")
    windplot(superFrameAugmented, "pm25_diff_winddirection", polar=False,
             useMedian=True, title="PM25 difference downwind - upwind", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotDownMinusUp")
    windplot(superFrameAugmented, "pm25", polar=True,
             useMedian=True, title="PM25 median all 6 luchtmeetnet stations", smooth=3,
             method="medianvalues", filename=projectdir+"/windplotAll")
    windplot(superFrameAugmented, "pm25", polar=True,
             useMedian=False, title="PM25 mean all 6 luchtmeetnet stations", smooth=3,
             method="meanvalues", filename=projectdir + "/windplotAllMean")
    windplot(superFrameAugmented, "pm25_NL49557", polar=True,
             useMedian=True, title="PM25 median Meetnet 49557 (North)", smooth=3,
             method="medianvalues", filename=projectdir + "/windplot557Median")
    windplot(superFrameAugmented, "pm25_NL49553", polar=True,
             useMedian=True, title="PM25 median Meetnet 49553 (North)", smooth=3,
             method="medianvalues", filename=projectdir + "/windplot553Median")
    windplot(superFrameAugmented, "pm25_NL49551", polar=True,
             useMedian=True, title="PM25 median Meetnet 49551 (South)", smooth=3,
             method="medianvalues", filename=projectdir + "/windplot551Median")

    return

# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



