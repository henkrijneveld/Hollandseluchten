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
KNMI_225 = pd.DataFrame()
HLL_549 = pd.DataFrame()
OZK_1845 = pd.DataFrame()
HLL_545 = pd.DataFrame()
NL49570 = pd.DataFrame()
OZK_1850 = pd.DataFrame()
startdate = "20230101"
enddate = "20230901"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/staartje-20231003"


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
def createSuperFrame(sensors, knmi):
    global superFrame
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

    superFrame = merged.copy()
#    superFrame.to_csv(projectdir + "/superFrame.csv", index=False)

    return merged

def diff_545_NL(aRow):
    high = aRow["pm25_HLL_545"]
    low = aRow["pm25_NL49570"]
    return high - low

def diff_549_NL(aRow):
    high = aRow["pm25_HLL_549"]
    low = aRow["pm25_NL49570"]
    return high - low

def diff_1850_NL(aRow):
    high = aRow["pm25_OZK_1850"]
    low = aRow["pm25_NL49570"]
    return high - low

def diff_1845_NL(aRow):
    high = aRow["pm25_OZK_1845"]
    low = aRow["pm25_NL49570"]
    return high - low


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

    superFrame["pm25_diff_545_NL"] = superFrame.apply(diff_545_NL, axis=1)
    superFrame["pm25_diff_549_NL"] = superFrame.apply(diff_549_NL, axis=1)
    superFrame["pm25_diff_1845_NL"] = superFrame.apply(diff_1845_NL, axis=1)
    superFrame["pm25_diff_1850_NL"] = superFrame.apply(diff_1850_NL, axis=1)

    superFrameAugmented = superFrame.copy()
    #superFrameAugmented.to_csv(projectdir + "/superFrameAugmented.csv", index=False)

    return superFrameAugmented


def runit():
    global superFrameAugmented

    allSensorsText = ["NL49570", "HLL_545", "HLL_549", "OZK_1845", "OZK_1850"]
    allSensors = convertTextToDataFrame(allSensorsText)

#    createTimeSeries_Multiple(list(zip(allSensors, allSensorsText)), projectdir, namesuffix="pm25")
    createSuperFrame(allSensorsText, KNMI_225)
    augmentSuperframe()

    attrPlot(superFrameAugmented, "pm25_diff_545_NL", binwidth=0.25, xlim=(-20, 60))
    attrPlot(superFrameAugmented, "pm25_diff_549_NL", binwidth=0.25, xlim=(-20, 60))
    attrPlot(superFrameAugmented, "pm25_diff_1845_NL", binwidth=0.25, xlim=(-20, 60))
    attrPlot(superFrameAugmented, "pm25_diff_1850_NL", binwidth=0.25, xlim=(-20, 60))
    diffPlot(HLL_545, HLL_549, attr="pm25", title="Difference 545 vs 549", xlim=(-10, 10))
    diffPlot(OZK_1845, OZK_1850, attr="pm25", title="Difference 1845 vs 1850", xlim=(-10, 10))
    diffPlot(HLL_545, OZK_1850, attr="pm25", title="Difference 545 vs 1850", xlim=(-10, 10))
    diffPlot(HLL_549, OZK_1850, attr="pm25", title="Difference 549 vs 1850", xlim=(-10, 10))
    diffPlot(HLL_545, OZK_1845, attr="pm25", title="Difference 545 vs 1845", xlim=(-10, 10))
    diffPlot(HLL_549, OZK_1845, attr="pm25", title="Difference 549 vs 1845", xlim=(-10, 10))



    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



