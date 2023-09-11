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
NLMedian = pd.DataFrame()

# Beverwijk set
KNMI_225 = pd.DataFrame()
NL49570 = pd.DataFrame()
HLL_545 = pd.DataFrame()
HLL_549 = pd.DataFrame()
OZK_1845 = pd.DataFrame()
OZK_1850 = pd.DataFrame()

# Zaandam set
KNMI_240 = pd.DataFrame()
NL49701 = pd.DataFrame()
HLL_420 = pd.DataFrame()
HLL_541 = pd.DataFrame()
OZK_1849 = pd.DataFrame()

# Industrial area Beverwijk
HLL_433 = pd.DataFrame() # westsensor
HLL_452 = pd.DataFrame() # eastsensor
HLL_513 = pd.DataFrame() # southsensor
HLL_226 = pd.DataFrame() # northsensor

# Extras
HLL_298 = pd.DataFrame()

startdate = "20230101"
enddate = "20230901"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/colocatie-2023"

def createTimeSeries(aCollection, namesuffix=""):
    for sensor in aCollection:
        sensordata = globals()[sensor]
        printSeries(sensordata, sensor + " " + namesuffix, projectdir + "/timeseries-" + sensor + "-" + namesuffix)


def comparePlot(leftFrame, rightFrame, knmiFrame, title, filename="", xlim=(-10, 10)):
    wfilename = filename
    dfilename = filename
    if filename:
        dfilename += "-difference"
        wfilename += "-windplot"
    diffPlot(leftFrame, rightFrame, xlim=xlim, attr="pm25", title=title, filename=dfilename)
    plotDiff25(leftFrame, rightFrame, title=title, knmiFrame=knmiFrame, filename=wfilename, smooth = 2)


def compareSameSensorsColocation():
    # comparison on:
    #   differenceplot
    #   deltawindplot
    comparePlot(HLL_545, HLL_549, KNMI_225, "HLL_545 vs HLL_549", filename=projectdir + "/same-HLL_545-HLL_549")
    comparePlot(HLL_420, HLL_541, KNMI_240, "HLL_420 vs HLL_541", filename=projectdir + "/same-HLL_420-HLL_541")
    comparePlot(OZK_1845, OZK_1850, KNMI_225, "OZK_1845 vs OZK_1850", filename=projectdir + "/same-OZK_1845-OZK_1850")

def compareDifferentTypesColocation():
    # Beverwijk: no much difference with same types, just take the first
    comparePlot(HLL_545, NL49570, KNMI_225, "HLL_545 vs NL49570", filename=projectdir + "/different-coloc-HLL_545-NL49570", xlim=(-20,20))
    comparePlot(HLL_545, OZK_1845, KNMI_225, "HLL_545 vs OZK_1845", filename=projectdir + "/different-coloc-HLL_545-OZK_1845", xlim=(-20,20))
    comparePlot(OZK_1845, NL49570, KNMI_225, "OZK_1845 vs NL49570", filename=projectdir + "/different-coloc-OZK_1845-NL49570", xlim=(-20,20))

    # Zaandam ignore 541 (too litte data
    comparePlot(HLL_420, NL49701, KNMI_225, "HLL_420 vs NL49701", filename=projectdir + "/different-coloc-HLL_420-NL49701", xlim=(-20,20))
    comparePlot(HLL_420, OZK_1849, KNMI_225, "HLL_420 vs OZK_1849", filename=projectdir + "/different-coloc-HLL_420-OZK_1849", xlim=(-20,20))
    comparePlot(OZK_1849, NL49701, KNMI_225, "OZK_1849 vs NL49701", filename=projectdir + "/different-coloc-OZK_1849-NL49701", xlim=(-20,20))

    # zaandam 541 on NL49701
    diffPlot(HLL_541, NL49701, xlim=(-20,20), attr="pm25", title="HLL_541 vs NL49701", filename=projectdir + "/different-coloc-HLL_541-NL49701-direction")
    diffPlot(HLL_541, OZK_1849, xlim=(-20,20), attr="pm25", title="HLL_541 vs OZK_1849", filename=projectdir + "/different-coloc-HLL_541-OZK_1849-direction")

    HLL_420_Before = removeDatesAfter(HLL_420, aDate="2023-04-01 00:00:00+00:00")
    HLL_420_After = removeDatesBefore(HLL_420, aDate="2023-04-15 00:00:00+00:00")
    diffPlot(HLL_420_Before, NL49701, xlim=(-20,20), attr="pm25", title="HLL_420 vs NL49701 before april 1", filename=projectdir + "/different-coloc-HLL_420-NL49701-before-1-april-direction")
    diffPlot(HLL_420_After, NL49701, xlim=(-20,20), attr="pm25", title="HLL_420 vs NL49701 after april 15", filename=projectdir + "/different-coloc-HLL_420-NL49701-after-15-april-direction")
    return

def runit():
    setBeverwijk = ["NL49570", "HLL_545", "HLL_549", "OZK_1845", "OZK_1850"]
    setZaandam = ["NL49701", "HLL_420", "HLL_541", "OZK_1849"]
    setIndustry = ["HLL_433", "HLL_452", "HLL_513", "HLL_226"] # west, east, south, north

# STEP 1: REVIEW CORE DATA

#    createTimeSeries(setBeverwijk, "Beverwijk")
#    createTimeSeries(setZaandam, "Zaandam")

    # outlier negatives on Beverwijk from 2023-07-15
#    reducedBeverwijk = removeDatesBefore(NL49570, aDate="2023-07-15 21:00:00+00:00")
#    printSeries(reducedBeverwijk, "NL49570 After 15 july 2023", projectdir + "/timeseries-49670-Beverwijk-negatives")

    # sensor 420 has a strangespike at 25 may 2023
#    HLL_420_Before = removeDatesAfter(HLL_420, aDate="2023-05-24 00:00:00+00:00")
#    HLL_420_After = removeDatesBefore(HLL_420, aDate="2023-05-26 00:00:00+00:00")
#    printSeries(HLL_420_Before, "HLL_420 Before 25 may spike", projectdir + "/timeseries-420-Zaandam-before-25may")
#    printSeries(HLL_420_After, "HLL_420 After 25 may spike", projectdir + "/timeseries-420-Zaandam-after-25may")

# STEP 2 compare same sensors
#    compareSameSensorsColocation()

# STEP 3 compare different sensors on colocation
#    compareDifferentTypesColocation()

# STEP 4 check "random" sensor against 541 to compare tails
#    comparePlot(HLL_298, HLL_545, KNMI_225, "HLL_298 (Zaandijk random) vs HLL_545", filename=projectdir + "/difference-HLL_298-HLL_545", xlim=(-20,20))
#    ==> tail seems to disappear

# STEP 5 Beverwijk area
    createTimeSeries(setIndustry, "Industry")
    comparePlot(HLL_433, HLL_452, KNMI_225, "HLL_433 (west) vs HLL_452 (east)", filename=projectdir + "/different-industry-west-east", xlim=(-20,20))
    comparePlot(HLL_513, HLL_226, KNMI_225, "HLL_513 (south) vs HLL_226 (north)", filename=projectdir + "/different-industry-south-north", xlim=(-20,20))

    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



