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
    global OZK_1845
    global OZK_1850
    merged = pd.DataFrame()

    # Both OVK's where in a different location in januari
    OZK_1845 = removeDatesBefore(OZK_1845, aDate="2023-02-01 21:00:00+00:00")
    OZK_1850 = removeDatesBefore(OZK_1850, aDate="2023-02-01 21:00:00+00:00")

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

#    attrPlot(superFrameAugmented, "pm25_diff_545_NL", binwidth=0.25, xlim=(-20, 60))
#    attrPlot(superFrameAugmented, "pm25_diff_549_NL", binwidth=0.25, xlim=(-20, 60))
#    attrPlot(superFrameAugmented, "pm25_diff_1845_NL", binwidth=0.25, xlim=(-20, 60))
#    attrPlot(superFrameAugmented, "pm25_diff_1850_NL", binwidth=0.25, xlim=(-20, 60))
    diffPlot(HLL_545, HLL_549, attr="pm25", title="Difference 545 vs 549", xlim=(-4, 4), describe=True)

    diffPlot(OZK_1845, OZK_1850, attr="pm25", title="Difference 1845 vs 1850", xlim=(-4, 4), describe=True)
#    diffPlot(HLL_545, OZK_1850, attr="pm25", title="Difference 545 vs 1850", xlim=(-10, 10))
#    diffPlot(HLL_549, OZK_1850, attr="pm25", title="Difference 549 vs 1850", xlim=(-10, 10))
#    diffPlot(HLL_545, OZK_1845, attr="pm25", title="Difference 545 vs 1845", xlim=(-10, 10))
#   diffPlot(HLL_549, OZK_1845, attr="pm25", title="Difference 549 vs 1845", xlim=(-10, 10))

    return
    simpleScatterPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_diff_545_NL",
                      xlim=(-15, 15), ylim=(-50, 50), title="Scatterplot describe test",
                      filename=projectdir+"/scatter-month-545Diff")


    monthmedians = superFrameAugmented.groupby(superFrameAugmented.datetime.dt.month).median()
    monthmedians["datetime"] = monthmedians.datetime.dt.month
    simpleScatterPlot(monthmedians, x="datetime", y="pm25_diff_545_NL",
                      xlim=(0, 10.0), ylim=(-50.0, 50.0), title="Scatterplot month - 545 Diff",
                      filename=projectdir+"/scatter-month-545Diff")

    simpleScatterPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_545",
                      xlim=(-20, 80), ylim=(-20.0, 80.0), title="Scatterplot NL - 545",
                      filename=projectdir+"/scatter-NL-545")

    scatter = sns.scatterplot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_549")
    scatter.set(title="Scatterplot NL - 549")
    scatter.set(xlim=(-20, 80))
    scatter.set(ylim=(-20, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="pm25_NL49570", y="pm25_diff_545_NL")
    scatter.set(title="Scatterplot NL - 545 Diff")
    scatter.set(xlim=(-20, 80))
    scatter.set(ylim=(-80, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="pm25_NL49570", y="pm25_diff_549_NL")
    scatter.set(title="Scatterplot NL - 549 Diff")
    scatter.set(xlim=(-20, 80))
    scatter.set(ylim=(-80, 80))
    plt.tight_layout()
    plt.show()



    scatter = sns.scatterplot(superFrameAugmented, x="winddirection", y="pm25_diff_545_NL")
    scatter.set(title="Scatterplot winddirection - 545 Diff")
    scatter.set(xlim=(5, 365))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="winddirection", y="pm25_diff_1845_NL")
    scatter.set(title="Scatterplot winddirection - 1845 Diff")
    scatter.set(xlim=(5, 365))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="windspeed", y="pm25_diff_545_NL")
    scatter.set(title="Scatterplot windspeed - 545 Diff")
    scatter.set(xlim=(0, 30))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="windspeed", y="pm25_diff_1845_NL")
    scatter.set(title="Scatterplot windspeed - 1845 Diff")
    scatter.set(xlim=(0, 30))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="temperature_HLL_545", y="pm25_diff_545_NL")
    scatter.set(title="Scatterplot temperature - 545 Diff")
    scatter.set(xlim=(-20, 60))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="temperature_OZK_1845", y="pm25_diff_1845_NL")
    scatter.set(title="Scatterplot temperature - 1845 Diff")
    scatter.set(xlim=(-20, 60))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()


    scatter = sns.scatterplot(superFrameAugmented, x="temperature_HLL_549", y="pm25_diff_549_NL")
    scatter.set(title="Scatterplot temperature - 549 Diff")
    scatter.set(xlim=(-20, 60))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="humidity_HLL_545", y="pm25_diff_545_NL")
    scatter.set(title="Scatterplot humidity - 545 Diff")
    scatter.set(xlim=(0, 100))
    scatter.set(ylim=(-50, 80))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="windspeed", y="humidity_HLL_545")
    scatter.set(title="Scatterplot windspeed - 545 humidity")
    scatter.set(xlim=(0, 30))
    scatter.set(ylim=(0, 100))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="windspeed", y="temperature_HLL_545")
    scatter.set(title="Scatterplot windspeed - 545 temperature")
    scatter.set(xlim=(0, 30))
    scatter.set(ylim=(-10, 40))
    plt.tight_layout()
    plt.show()

    scatter = sns.scatterplot(superFrameAugmented, x="windspeed", y="winddirection")
    scatter.set(title="Scatterplot windspeed - winddirection")
    scatter.set(xlim=(0, 30))
    scatter.set(ylim=(0, 370 ))
    plt.tight_layout()
    plt.show()


    # only select the tail for 545 difference NL > 10
    tempSelection = superFrameAugmented[(superFrameAugmented['temperature_HLL_545'] > 17) &
                                        (superFrameAugmented['temperature_HLL_545'] < 23)]
    tempSelection = tempSelection.reset_index(drop=True)

    scatter = sns.scatterplot(superFrameAugmented, x="temperature_HLL_545", y="pm25_NL49570")
    scatter.set(title="Scatterplot temperature - 49570")
    scatter.set(xlim=(-20, 40))
    scatter.set(ylim=(-10, 50))
    plt.tight_layout()
    plt.show()





    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



