# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

# STAARTEN, WINDPUFJES EN GOUDEN STANDAARDS

import sys

import matplotlib.pyplot as plt

sys.path.insert(0, '../..')
from analyzer import *
from plotter import *
import math
import pprint as pp

# General
wideFrame = pd.DataFrame()
wideFrameAugmented = pd.DataFrame()
HLL_326 = pd.DataFrame()
HLL_298 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
HLL_320 = pd.DataFrame()
HLL_415 = pd.DataFrame()
HLL_378 = pd.DataFrame()
HLL_339 = pd.DataFrame()
HLL_325 = pd.DataFrame()
startdate = "20230101"
enddate = "20231001"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/koog-20231010"

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
            sensorFrame.drop_duplicates(inplace=True, ignore_index=True)
            merged = pd.merge(merged, sensorFrame, how='outer', on='datetime',
                              suffixes=("", "_" + sensor))
            merged.drop(['sensorname'+'_'+sensor], axis=1, inplace=True)
    merged.drop(['sensorname'], axis=1, inplace=True)
    # delete 0 and 990
    knmi = knmi[(knmi["winddirection"] < 369) & (knmi["winddirection"] > 5)]
    merged = pd.merge(merged, knmi, on='datetime', 
                      suffixes=("", "_knmi"))
    merged.drop(['sensorname', "pm25", "temperature", "humidity"], axis=1, inplace=True)
#    merged.drop(merged.columns[0], axis=1, inplace=True)

    wideFrame = merged.copy()
#    superFrame.to_csv(projectdir + "/superFrame.csv", index=False)

    return merged


def highhumidity(aRow):
    humidity = aRow["humidity_HLL_298"]
    return humidity > 80

def diff_298_326(aRow):
    value = aRow["pm25_HLL_298"]
    compare = aRow["pm25_HLL_326"]
    return value - compare

def diff_326_320(aRow):
    value = aRow["pm25_HLL_326"]
    compare = aRow["pm25_HLL_320"]
    return value - compare
def diff_298_320(aRow):
    value = aRow["pm25_HLL_298"]
    compare = aRow["pm25_HLL_320"]
    return value - compare


# add columns:
#
# write result to superFrameAugmented.csv
def augmentWideFrame():
    global wideFrameAugmented

    wideFrame["diff_298_326"] = wideFrame.apply(diff_298_326, axis=1)
    wideFrame["diff_326_320"] = wideFrame.apply(diff_326_320, axis=1)
    wideFrame["diff_298_320"] = wideFrame.apply(diff_298_320, axis=1)

    print("Attributes added")

    wideFrameAugmented = wideFrame.copy()
    print("Frame copied")
    #wideFrameAugmented.to_csv(projectdir + "/wideFrameAugmented.csv", index=False)

    return wideFrameAugmented


def runit():
    global wideFrameAugmented

    allSensorsText = ["HLL_326", "HLL_298", "HLL_320", "HLL_415",
                      "HLL_378", "HLL_339", "HLL_325"]

#    allSensors = convertTextToDataFrame(allSensorsText)
#    createTimeSeries_Multiple(list(zip(allSensors, allSensorsText)), projectdir, namesuffix="pm25")

    createWideFrame(allSensorsText, KNMI_240)
    print("Wideframe created")
    augmentWideFrame()
    print("Wideframe augmented")

#    diffPlot(HLL_298, HLL_339, "pm25", title="Diffplot 298 vs 339", xlim=(-10,10))
    diffPlot(HLL_298, HLL_326, "pm25", title="Diffplot 298 vs 326", xlim=(-10,10))
    diffPlot(HLL_326, HLL_320, "pm25", title="Diffplot 326 vs 320", xlim=(-10,10))
    diffPlot(HLL_298, HLL_320, "pm25", title="Diffplot 298 vs 320", xlim=(-10,10))


#    diffPlot(HLL_298, HLL_320, "pm25", title="Diffplot 298 vs 320", xlim=(-10,10))
#    diffPlot(HLL_298, HLL_415, "pm25", title="Diffplot 298 vs 415", xlim=(-10,10))
#    diffPlot(HLL_298, HLL_378, "pm25", title="Diffplot 298 vs 378", xlim=(-10,10))
#    diffPlot(HLL_298, HLL_325, "pm25", title="Diffplot 298 vs 325", xlim=(-10,10))
    simpleScatterPlot(wideFrameAugmented, x="humidity_HLL_298", y="humidity_HLL_326", xlim=(20,100), ylim=(20,100))
    simpleScatterPlot(wideFrameAugmented, x="temperature_HLL_298", y="temperature_HLL_326", xlim=(-10,50), ylim=(-10,50))

    windplot(wideFrameAugmented, "diff_298_326")
    windplot(wideFrameAugmented, "diff_326_320")
    windplot(wideFrameAugmented, "diff_298_320")


    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



