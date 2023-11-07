# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

# STAARTEN, WINDPUFJES EN GOUDEN STANDAARDS

import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model


import matplotlib.pyplot as plt

sys.path.insert(0, '../..')
from analyzer import *
from plotter import *
import math
import pprint as pp

type = "outer"
def getMergetype():
    global type
    return type


# General
wideFrame = pd.DataFrame()
wideFrameAugmented = pd.DataFrame()
KNMI_225 = pd.DataFrame()
HLL_549 = pd.DataFrame()
NL49701 = pd.DataFrame()
HLL_541 = pd.DataFrame()
HLL_545 = pd.DataFrame()
HLL_420 = pd.DataFrame()
NL49570 = pd.DataFrame()
startdate = "20230101"
enddate = "20231001"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/Machine-Learning-20231106"
sensorList = ["wideFrameAugmented", "KNMI_225", "HLL_549", "NL49701", "HLL_541", "HLL_545", "HLL_420", "NL49570"]

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
            merged = pd.merge(merged, sensorFrame, how=getMergetype(), on='datetime',
                              suffixes=("", "_" + sensor), validate="1:1")
            merged.drop(['sensorname'+'_'+sensor], axis=1, inplace=True)
    merged.drop(['sensorname'], axis=1, inplace=True)
    # delete 0 and 990
    knmi = knmi[(knmi["winddirection"] < 369) & (knmi["winddirection"] > 5)]
    merged = pd.merge(merged, knmi, on='datetime', how=getMergetype(),
                      suffixes=("", "_knmi"), validate="1:1")
    merged.drop(['sensorname', "pm25", "temperature", "humidity"], axis=1, inplace=True)
#    merged.drop(merged.columns[0], axis=1, inplace=True)

    wideFrame = merged.copy()
#    superFrame.to_csv(projectdir + "/superFrame.csv", index=False)

    return merged


def augmentWideFrame(sensorList):
    global wideFrame
    global wideFrameAugmented

    wideFrameAugmented = wideFrame.copy()
    wideFrameAugmented.to_csv(projectdir + "/wideFrameAugmented.csv", index=False)

    return wideFrameAugmented

def numpyfi(aFrame, sensorlist, targetlist, datalist):
    fillFrame = aFrame.copy()
    fillFrame = fillFrame[sensorlist].dropna()
    target = fillFrame[targetlist].to_numpy(copy=True)
    data = fillFrame[datalist].to_numpy(copy=True)
    return (target, data)

def plotdiff(left, right, title):
    target_diff = left - right
    plt.hist(target_diff, bins=np.arange(-10, 10, 0.5))
    plt.title(title)
    plt.show()



def caphum(aFrame, maxhum):
    aFrame = aFrame[aFrame["humidity"] < maxhum]
    return aFrame

def runit():
    global wideFrameAugmented
    global wideFrame

    global HLL_545
    global HLL_549
    global HLL_541
    global HLL_420


    allSensorsText = ["HLL_545", "HLL_549", "HLL_420", "HLL_541", "NL49570", "NL49701"]

    maxhum = 90
    HLL_545 = caphum(HLL_545, maxhum)
    HLL_549 = caphum(HLL_549, maxhum)
    HLL_541 = caphum(HLL_541, maxhum)
    HLL_420 = caphum(HLL_420, maxhum)

    printf("1. wideFrame: %d\n", len(wideFrame))
    allSensors = convertTextToDataFrame(allSensorsText)
#    createTimeSeries_Multiple(list(zip(allSensors, allSensorsText)), projectdir, namesuffix="pm25")
    createWideFrame(allSensorsText, KNMI_225)
    printf("2. wideFrame: %d\n", len(wideFrame))
    augmentWideFrame(allSensors)
    printf("3. wideFrame: %d\n", len(wideFrame))

#    diffPlot(HLL_545, NL49570, attr="pm25", xlim=(-15,15), title="Uncalibrated diff 545 vs 49570", binwidth=0.25)
#    diffPlot(HLL_549, NL49570, attr="pm25", xlim=(-15,15), title="Uncalibrated diff 549 vs 49570", binwidth=0.25)
#    diffPlot(HLL_545, HLL_549, attr="pm25", xlim=(-15,15), title="Uncalibrated diff 545 vs 549", binwidth=0.25)
    diffPlot(HLL_541, NL49701, attr="pm25", xlim=(-10,10), title="Uncalibrated diff 541 vs 49701", binwidth=0.5)
    diffPlot(HLL_420, NL49701, attr="pm25", xlim=(-10,10), title="Uncalibrated diff 420 vs 49701", binwidth=0.5)
    diffPlot(HLL_420, HLL_541, attr="pm25", xlim=(-10,10), title="Uncalibrated diff 420 vs 541", binwidth=0.5)
    printf("#420 uncal: %d\n", len(HLL_420))

    # make arrays in numpy format. Maybe not necessary, we will see later
    target, data = numpyfi(wideFrameAugmented,
            ["pm25_NL49570", "pm25_HLL_545", "temperature_HLL_545", "humidity_HLL_545"],
            "pm25_NL49570",
            ["pm25_HLL_545", "temperature_HLL_545", "humidity_HLL_545"])

    # split
    data_train, data_test, target_train, target_test = train_test_split(data, target, random_state=0)

    # model Lasso according to cheat sheet
    trans = PolynomialFeatures(degree=2)
    data_train = trans.fit_transform(data_train)
#    reg = linear_model.Lasso(alpha=0.5)
#    reg = linear_model.ElasticNet(random_state=0)
#    reg = linear_model.Ridge(alpha=10)
    reg = linear_model.BayesianRidge(tol=1e-3, fit_intercept=False, compute_score=True)
    reg.set_params(alpha_init=10, lambda_init=6)

    reg.fit(data_train, target_train)
    printf("5 wideFrameAugmented: %d\n", len(wideFrameAugmented))

    # blackbox accuracy score
    data_test = trans.fit_transform(data_test)
    print(reg.score(data_test, target_test))

    # build predicted array, compare with test
    target_predicted = reg.predict(data_test)

    # difference
#    target_diff = target_predicted - target_test
#    plt.hist(target_diff, bins=np.arange(-15, 15, 0.25))
#    plt.title("Histo 545 vs NL")
#    plt.show()

    # do it for the other one
    target, data = numpyfi(wideFrameAugmented,
            ["pm25_NL49570", "pm25_HLL_549", "temperature_HLL_549", "humidity_HLL_549"],
            "pm25_NL49570",
            ["pm25_HLL_549", "temperature_HLL_549", "humidity_HLL_549"])

    # build predicted array, compare with test
    data = trans.fit_transform(data)
    target_predicted = reg.predict(data)
    printf("4 wideFrameAugmented: %d\n", len(wideFrameAugmented))

    # difference
#    target_diff = target_predicted - target
#    plt.hist(target_diff, bins=np.arange(-15, 15, 0.25))
#    plt.title("Histo 549 vs NL")
#    plt.show()

    # compare the two HLL
    data_545, data_549 = numpyfi(wideFrameAugmented,
            ["pm25_HLL_549", "temperature_HLL_549", "humidity_HLL_549", "pm25_HLL_545", "temperature_HLL_545", "humidity_HLL_545"],
            ["pm25_HLL_545", "temperature_HLL_545", "humidity_HLL_545"],
            ["pm25_HLL_549", "temperature_HLL_549", "humidity_HLL_549"])
    data_545 = trans.fit_transform(data_545)
    data_549 = trans.fit_transform(data_549)

    data_545_cal = reg.predict(data_545)
    data_549_cal = reg.predict(data_549)
    plotdiff(data_545_cal, data_549_cal, "Histo calibrated 545 vs 549")
    printf("3 wideFrameAugmented: %d\n", len(wideFrameAugmented))

    # compare 541 to NL
    data_49701, data_541 = numpyfi(wideFrameAugmented,
            ["pm25_HLL_541", "temperature_HLL_541", "humidity_HLL_541", "pm25_NL49701"],
            "pm25_NL49701",
            ["pm25_HLL_541", "temperature_HLL_541", "humidity_HLL_541"])
    data_541 = trans.fit_transform(data_541)

    data_541_cal = reg.predict(data_541)

    plotdiff(data_541_cal, data_49701, "Histo calibrated 541 vs NL")

    printf("2 wideFrameAugmented: %d\n", len(wideFrameAugmented))

    # compare 541 to 420
    data_49701, data_420 = numpyfi(wideFrameAugmented,
            ["pm25_HLL_420", "temperature_HLL_420", "humidity_HLL_420", "pm25_NL49701"],
            "pm25_NL49701",
            ["pm25_HLL_420", "temperature_HLL_420", "humidity_HLL_420"])
    data_420 = trans.fit_transform(data_420)
    printf("#420 fit: %d\n", len(data_420))

    data_420_cal = reg.predict(data_420)
    printf("1 wideFrameAugmented: %d\n", len(wideFrameAugmented))
    printf("#420 cal: %d\n", len(data_420_cal))

    plotdiff(data_420_cal, data_49701, "Histo calibrated 420 vs NL")


    # compare 541 to 420
    data_541, data_420 = numpyfi(wideFrameAugmented,
            ["pm25_HLL_420", "temperature_HLL_420", "humidity_HLL_420",
                    "pm25_HLL_541", "temperature_HLL_541", "humidity_HLL_541"],
            ["pm25_HLL_541", "temperature_HLL_541", "humidity_HLL_541"],
            ["pm25_HLL_420", "temperature_HLL_420", "humidity_HLL_420"])
    data_420 = trans.fit_transform(data_420)
    printf("#420 fit: %d\n", len(data_420))
    data_420_cal = reg.predict(data_420)

    data_541 = trans.fit_transform(data_541)
    printf("#541 fit: %d\n", len(data_541))
    data_541_cal = reg.predict(data_541)


    plotdiff(data_420_cal, data_541_cal, "Histo calibrated 420 vs 541")

    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#   printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



