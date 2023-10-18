# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

# STAARTEN, WINDPUFJES EN GOUDEN STANDAARDS

import sys

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, '../..')
from analyzer import *
from plotter import *
import math
import pprint as pp

# General
wideFrame = pd.DataFrame()
wideFrameAugmented = pd.DataFrame()
HLL_256 = pd.DataFrame()
HLL_326 = pd.DataFrame()
HLL_298 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
HLL_320 = pd.DataFrame()
HLL_415 = pd.DataFrame()
HLL_378 = pd.DataFrame()
HLL_339 = pd.DataFrame()
HLL_325 = pd.DataFrame()
HLL_323 = pd.DataFrame()
HLL_413 = pd.DataFrame()
HLL_345 = pd.DataFrame()
NL49701 = pd.DataFrame()
NLMedian = pd.DataFrame()
startdate = "20230101"
enddate = "20231001"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/koog-20231010"

hllNumberlist = ["298", "326", "320", "415", "378", "339", "325"]
hllGrootkruislist = ["345", "413", "415", "323"]

def convertTextToDataFrame(aTextCollection):
    aDataFrameCollection = []
    for sensor in aTextCollection:
        aDataFrameCollection.append(globals()[sensor])
    return aDataFrameCollection

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
def createWideFrame(sensors, knmi):
    global wideFrame

    merged = pd.DataFrame()

    for sensor in sensors:
        sensorFrame = globals()[sensor]
        sensorFrame.drop_duplicates(inplace=True, ignore_index=True)

        if merged.empty:
            merged = sensorFrame.copy()
            # these columns will be removed later. Used to ease the addition
            # of sensor-name suffixes
            # Oh and @todo: this can be done shorter, I know.
            if not "pm25" in merged.columns:
                merged["pm25"] = math.nan
            else:
                merged.rename(columns={'pm25': 'pm25_' + sensor}, inplace=True)
                merged["pm25"] = math.nan
            if not "temperature" in merged.columns:
                merged["temperature"] = math.nan
            else:
                merged.rename(columns={'temperature': 'temperature_' + sensor}, inplace=True)
                merged["temperature"] = math.nan
            if not "humidity" in merged.columns:
                merged["humidity"] = math.nan
            else:
                merged.rename(columns={'humidity': 'humidity_' + sensor}, inplace=True)
                merged["humidity"] = math.nan
        else:
#            sensorFrame.drop_duplicates(inplace=True, ignore_index=True)
            merged = pd.merge(merged, sensorFrame, how='outer', on='datetime',
                              suffixes=("", "_" + sensor), validate="1:1")
            merged.drop(['sensorname'+'_'+sensor], axis=1, inplace=True)
    merged.drop(['sensorname'], axis=1, inplace=True)
    # delete 0 and 990
    knmi = knmi[(knmi["winddirection"] < 369) & (knmi["winddirection"] > 5)]
    merged = pd.merge(merged, knmi, on='datetime', 
                      suffixes=("", "_knmi"), validate="1:1")
    merged.drop(['sensorname', "pm25", "temperature", "humidity"], axis=1, inplace=True)
#    merged.drop(merged.columns[0], axis=1, inplace=True)

    wideFrame = merged.copy()
#    superFrame.to_csv(projectdir + "/superFrame.csv", index=False)

    return merged


def highhumidity(aRow):
    humidity = aRow["humidity_HLL_298"]
    return humidity > 80

# add columns:
#
# write result to superFrameAugmented.csv
def augmentWideFrame():
    global wideFrame
    global wideFrameAugmented

    createDiffColumn(wideFrame, "pm25_HLL_298", "pm25_HLL_326", "diff_298_326")
    createDiffColumn(wideFrame, "pm25_HLL_326", "pm25_HLL_320", "diff_326_320")
    createDiffColumn(wideFrame, "pm25_HLL_298", "pm25_HLL_320", "diff_298_320")
    createDiffColumn(wideFrame, "pm25_HLL_298", "pm25_HLL_378", "diff_298_378")
    createDiffColumn(wideFrame, "pm25_HLL_345", "pm25_HLL_325", "diff_345_325")


#    wideFrame["highhumidity"] = wideFrame.apply(highhumidity, axis=1)

    wideFrame["highhumidity"] = wideFrame["humidity_HLL_298"] > 80

    wideFrame = wideFrame[wideFrame["humidity_HLL_298"] < 80]

    # compare to median
    for sensor in hllNumberlist:
        createDiffColumn(wideFrame, "pm25_HLL_"+sensor, "pm25_NLMedian", "diff_"+sensor+"_NLMedian")

    wideFrame['datehour'] = wideFrame['datetime'].dt.hour
    wideFrame['dateday'] = wideFrame['datetime'].dt.day_name()  # monday = 0

    print("Attributes added")

    wideFrameAugmented = wideFrame.copy()
    print("Frame copied")
    wideFrameAugmented.to_csv(projectdir + "/wideFrameAugmented.csv", index=False)

    return wideFrameAugmented


def runit():
    global wideFrame
    global wideFrameAugmented

    allSensorsText = ["HLL_339", "HLL_298", "HLL_326", "HLL_320", "NLMedian"]
    allSensorsTextAlt=["HLL_378", "HLL_415", "HLL_325", "HLL_298", "NLMedian"]
    allSensorsGrootkruis=["HLL_323", "HLL_345", "HLL_413", "HLL_415", "NLMedian"]

    allSensorsTxt = ["HLL_339", "HLL_298", "HLL_326", "HLL_320", "NLMedian",
                     "HLL_378", "HLL_415", "HLL_325", "HLL_323", "HLL_345", "HLL_413"]

    allSensors = convertTextToDataFrame(allSensorsGrootkruis)
#    createTimeSeries_Multiple(list(zip(allSensors, allSensorsGrootkruis)), projectdir, namesuffix="pm25",
#                              fname="timeseries-grootkruis")
    createWideFrame(allSensorsTxt, KNMI_240)
    augmentWideFrame()

    simpleStripPlot(wideFrame, "datehour", "pm25_HLL_325", xlim=(-1,24), ylim=(0,40),
                    title="HLL 325 dagelijkse gang", xfont=12)

    simpleStripPlot(wideFrame, "datehour", "pm25_HLL_345", xlim=(-1,24), ylim=(0,40),
                    title="HLL 345 dagelijkse gang", xfont=12)

    simpleStripPlot(wideFrame, "datehour", "diff_345_325", xlim=(-1,24), ylim=(-10,10),
                    title="Diff 345 vs 325 dagelijkse gang", xfont=12)

    simpleStripPlot(wideFrame, "datehour", "diff_298_320", xlim=(-1,24), ylim=(-10,10),
                    title="Diff 298 vs 320 dagelijkse gang", xfont=12)


    return
    # DIFFSENSORS
    diffPlotSensors(wideFrame, "pm25", allSensorsGrootkruis, projectdir+"/diffplots-grootkruis")

    # WINDPLOTS
    diffWindPlotSensors(wideFrame, "pm25", allSensorsGrootkruis, projectdir+"/windplots-grootkruis", smooth=3)
    windplot(wideFrameAugmented, "pm25_HLL_345", polar=True,
             method="medianvalues", smooth=0, title="pm25 HLL 345")

    return
    windplot(wideFrameAugmented, "diff_298_378", polar=True, smooth=3, title="diff_298_378")
    windplot(wideFrameAugmented, "diff_298_NLMedian", polar=True, smooth=3, title="diff_298_NLMedian")
    windplot(wideFrameAugmented, "diff_378_NLMedian", polar=True, smooth=3, title="diff_378_NLMedian")

    printSeries(NLMedian)

    windplot(wideFrameAugmented, "temperature_HLL_298", smooth=3,
             title="humidity 298", method="medianvalues")

    for sensor in hllNumberlist:
        windplot(wideFrameAugmented, "diff_"+sensor+"_NL49701",
                 polar=False, smooth=3, method="medianvalues",
                 title="HLL "+sensor+" vs. NL49701")

    return
    #    diffPlot(HLL_298, HLL_339, "pm25", title="Diffplot 298 vs 339", xlim=(-10,10))
    diffPlot(HLL_298, NL49701, "pm25", title="Diffplot 298 vs NL49701", xlim=(-10,10))
    diffPlot(HLL_326, NL49701, "pm25", title="Diffplot 326 vs NL49701", xlim=(-10,10))
    diffPlot(HLL_320, NL49701, "pm25", title="Diffplot 320 vs NL49701", xlim=(-10,10))

    simpleJointPlot(wideFrameAugmented, "pm25_HLL_298", "pm25_HLL_326",
                    xlim=(0,40), ylim=(0,40),title="298 vs 326", hue="highhumidity",
                    dotsize=40)

#    diffPlot(HLL_298, HLL_320, "pm25", title="Diffplot 298 vs 320", xlim=(-10,10))
#    diffPlot(HLL_298, HLL_415, "pm25", title="Diffplot 298 vs 415", xlim=(-10,10))
#    diffPlot(HLL_298, HLL_378, "pm25", title="Diffplot 298 vs 378", xlim=(-10,10))
#    diffPlot(HLL_298, HLL_325, "pm25", title="Diffplot 298 vs 325", xlim=(-10,10))
    simpleScatterPlot(wideFrameAugmented, x="humidity_HLL_298", y="humidity_HLL_326",
                      xlim=(20,100), ylim=(20,100))
    simpleScatterPlot(wideFrameAugmented, x="temperature_HLL_298", y="temperature_HLL_326",
                      xlim=(-10,50), ylim=(-10,50))

    windplot(wideFrameAugmented, "diff_298_326", polar=False, smooth=2, method="medianvalues")
    windplot(wideFrameAugmented, "diff_326_320", polar=False, smooth=2)
    windplot(wideFrameAugmented, "diff_298_320", polar=False, smooth=2)


    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



