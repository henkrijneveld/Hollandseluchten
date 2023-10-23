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

type = "inner"
def getType():
    global type
    return type


# General
superFrame = pd.DataFrame()
superFrameAugmented = pd.DataFrame()
KNMI_225 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
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
    global HLL_545
    merged = pd.DataFrame()

    # Both OVK's where in a different location in januari
    OZK_1845 = removeDatesBefore(OZK_1845, aDate="2023-02-01 21:00:00+00:00")
    OZK_1850 = removeDatesBefore(OZK_1850, aDate="2023-02-01 21:00:00+00:00")

    # mean outer: delta hum: 30 / delta pm: 7 / zeropoint (delta pm = 0) on hum 52
#    HLL_545["pm25"] = HLL_545["pm25"] + ((52 - HLL_545["humidity"]) * 7 / 30)
#    HLL_545["pm25"] = HLL_545["pm25"] + ((60 - HLL_545["humidity"]) * 2 / 23)

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
            merged = pd.merge(merged, sensorFrame, how=getType(), on='datetime',
                              suffixes=("", "_" + sensor))
            merged.drop(['sensorname'+'_'+sensor], axis=1, inplace=True)
    merged.drop(['sensorname'], axis=1, inplace=True)
    # delete 0 and 990
    knmi = knmi[(knmi["winddirection"] < 369) & (knmi["winddirection"] > 5)]
    merged = pd.merge(merged, knmi, on='datetime', how=getType(),
                      suffixes=("", "_knmi"))
    merged.drop(['sensorname', "pm25", "temperature", "humidity"], axis=1, inplace=True)
#    merged.drop(merged.columns[0], axis=1, inplace=True)

    superFrame = merged.copy()
#    superFrame.to_csv(projectdir + "/superFrame.csv", index=False)

# windspeed correction
#    superFrame["pm25_HLL_545"] = superFrame["pm25_HLL_545"] + (superFrame["windspeed"] - 10)

    return superFrame

def diff_545_NL(aRow):
    high = aRow["pm25_HLL_545"]
    low = aRow["pm25_NL49570"]
    return high - low

def diff_549_NL(aRow):
    high = aRow["pm25_HLL_549"]
    low = aRow["pm25_NL49570"]
    return high - low

def diff_545_549(aRow):
    high = aRow["pm25_HLL_545"]
    low = aRow["pm25_HLL_549"]
    return high - low

def diff_1850_NL(aRow):
    high = aRow["pm25_OZK_1850"]
    low = aRow["pm25_NL49570"]
    return high - low

def diff_1845_NL(aRow):
    high = aRow["pm25_OZK_1845"]
    low = aRow["pm25_NL49570"]
    return high - low

def diff_545_1845(aRow):
    high = aRow["pm25_HLL_545"]
    low = aRow["pm25_OZK_1845"]
    return high - low

def highhumidity(aRow):
    humidity = aRow["humidity_HLL_545"]
    return humidity > 85

def humiditycat(aRow):
    humidity = aRow["humidity_HLL_545"]
    if math.isfinite(humidity):
        return int(humidity/10 + 0.5)
    else:
        return 0

def windspeedcat(aRow):
    wspeed = aRow["windspeed"]
    if math.isfinite(wspeed):
        return int(wspeed)
    else:
        return 0



# add columns:
#   pm25_diff_WE
#   pm25_diff_NS
#   pm25_diff_coloc (diff to NL49553 - NL49557)
#   pm25_upwind (pm25 without the local source)
#   pm25_diff_winddirection (pm25 difference in winddirection)
#
# write result to superFrameAugmented.csv
def augmentSuperframe():
    global superFrame
    global superFrameAugmented

    superFrame["pm25_diff_545_NL"] = superFrame.apply(diff_545_NL, axis=1)
#    superFrame["pm25_diff_549_NL"] = superFrame.apply(diff_549_NL, axis=1)
    superFrame["pm25_diff_1845_NL"] = superFrame.apply(diff_1845_NL, axis=1)
#    superFrame["pm25_diff_1850_NL"] = superFrame.apply(diff_1850_NL, axis=1)
    superFrame["pm25_diff_545_549"] = superFrame.apply(diff_545_549, axis=1)
    superFrame["pm25_diff_545_1845"] = superFrame.apply(diff_545_1845, axis=1)

    superFrame["highhumidity"] = superFrame.apply(highhumidity, axis=1)
#   superFrame=superFrame[superFrame["highhumidity"] == False]

    superFrame["quotient"] = superFrame["pm25_HLL_545"] / superFrame["pm25_NL49570"]

    superFrame["windspeedcat"] = superFrame.apply(windspeedcat, axis=1)
    superFrame["humiditycat"] = superFrame.apply(humiditycat, axis=1)

    #superFrameAugmented.to_csv(projectdir + "/superFrameAugmented.csv", index=False)

    superFrame['datehour'] = superFrame['datetime'].dt.hour
    superFrame['dateday'] = superFrame['datetime'].dt.day_name()  # monday = 0

    superFrameAugmented = superFrame.copy()

    return superFrameAugmented


def runit():
    global superFrameAugmented
    global HLL_545
    global HLL_549

    allSensorsText = ["HLL_545", "HLL_549", "OZK_1845", "OZK_1850", "NL49570"]

    allSensors = convertTextToDataFrame(allSensorsText)
#    createTimeSeries_Multiple(list(zip(allSensors, allSensorsText)), projectdir, namesuffix="pm25")
    createSuperFrame(allSensorsText, KNMI_225)
    augmentSuperframe()

    superFrameAugmented80plus = superFrameAugmented.copy()
    superFrameAugmented80plus = superFrameAugmented80plus[superFrameAugmented80plus["highhumidity"] == True]
    superFrameAugmented80min = superFrameAugmented.copy()
    superFrameAugmented80min = superFrameAugmented80min[superFrameAugmented80min["highhumidity"] != True]

    plotframe = medianvalues([superFrameAugmented], "datehour", "pm25_diff_545_NL")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_diff_545_NL", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily verschil 545 vs NL")
    lplot.set_ylabel("Difference median", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-pm25-diff-hour-545-NL-median-"+getType()+".jpg")
    plt.show()

    plotframe = medianvalues([superFrameAugmented], "datehour", "pm25_diff_1845_NL")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_diff_1845_NL", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily verschil 1845 vs NL")
    lplot.set_ylabel("Difference median", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-pm25-diff-hour-1845-NL-median-"+getType()+".jpg")
    plt.show()

    plotframe = medianvalues([superFrameAugmented], "datehour", "pm25_HLL_545")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_HLL_545", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily absolute pm25 HLL 545")
    lplot.set_ylabel("PM25 median", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-pm25-pm25-hour-545-median-"+getType()+".jpg")
    plt.show()

    plotframe = medianvalues([superFrameAugmented], "datehour", "humidity_HLL_545")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="humidity_HLL_545", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily humidity 545")
    lplot.set_ylabel("Humidity mean", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-humidity-hour-545-median-"+getType()+".jpg")
    plt.show()

    plotframe = meanvalues([superFrameAugmented], "datehour", "windspeed")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="windspeed", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily windspeed")
    lplot.set_ylabel("Windspeed m/s mean", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-windspeed-mean-"+getType()+".jpg")
    plt.show()

    plotframe = meanvalues([superFrameAugmented], "datehour", "pm25_diff_545_NL")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_diff_545_NL", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily verschil 545 vs NL")
    lplot.set_ylabel("Difference mean", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-pm25-diff-hour-545-NL-mean-"+getType()+".jpg")
    plt.show()

    plotframe = meanvalues([superFrameAugmented], "datehour", "pm25_HLL_545")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_HLL_545", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily absolute pm25 HLL 545")
    lplot.set_ylabel("PM25 median", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-pm25-pm25-hour-545-mean-"+getType()+".jpg")
    plt.show()

    plotframe = meanvalues([superFrameAugmented], "datehour", "humidity_HLL_545")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="humidity_HLL_545", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily humidity 545")
    lplot.set_ylabel("Humidity mean", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-humidity-hour-545-mean-"+getType()+".jpg")
    plt.show()

    plotframe = meanvalues([superFrameAugmented], "datehour", "temperature_HLL_545")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="temperature_HLL_545", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily temperature 545")
    lplot.set_ylabel("temperature mean", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-temperature-hour-545-mean-"+getType()+".jpg")
    plt.show()


    plotframe = meanvalues([superFrameAugmented], "datehour", "pm25_NL49570")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_NL49570", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily NL49570")
    lplot.set_ylabel("pm25 mean NL49570", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-pm25-NL49570-mean-"+getType()+".jpg")
    plt.show()



    plotframe = meanvalues([superFrameAugmented], "datehour", "pm25_diff_1845_NL")
    lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_diff_1845_NL", linewidth=2.5))
    lplot.set(xlim=(-1, 24))
    lplot.set(title="Daily verschil 1845 vs NL")
    lplot.set_ylabel("Difference mean", fontsize=14)
    lplot.set_xlabel("Hour of day (UTC)", fontsize=14)
    plt.tight_layout()
    lplot.get_figure().savefig(projectdir + "/0-9-pm25-diff-hour-1845-NL-mean-"+getType()+".jpg")
    plt.show()



    return

    diffPlotSensors(superFrameAugmented, "pm25", allSensorsText, title="Delta pm25: All sensors and all humidity "+type,
                    fname=projectdir + "/0-0-diffplots-sensors-allhum"+"-"+type)
    diffWindPlotSensors(superFrameAugmented, "pm25", allSensorsText, title="Delta pm25: All sensors and all humidity "+type,
                        fname=projectdir + "/0-1-windplots-sensors-allhum"+"-"+type, smooth=3)
    diffWindPlotSensors(superFrameAugmented80plus, "pm25", allSensorsText, title="Delta pm25: All sensors and humidity > 80 "+type,
                        fname=projectdir + "/0-2-windplots-sensors-80plus"+"-"+type, smooth=3)
    diffWindPlotSensors(superFrameAugmented80min, "pm25", allSensorsText, title="Delta pm25: All sensors and all humidity < 80 "+type,
                        fname=projectdir + "/0-3-windplots-sensors-80min"+"-"+type, smooth=3)

    windplot(superFrameAugmented, "windspeed", polar=False,
             useMedian=True, title="Windspeed "+type, smooth=3,
             method="medianvalues", filename=projectdir+"/0-4-windplot-windspeed-allhum"+"-"+type)
    windplot(superFrameAugmented80plus, "windspeed", polar=False,
             useMedian=True, title="Windspeed humidity > 80 "+type, smooth=3,
             method="medianvalues", filename=projectdir+"/0-5-windplot-windspeed-80plus"+"-"+type)
    windplot(superFrameAugmented80min, "windspeed", polar=False,
             useMedian=True, title="Windspeed humidity < 80 "+type, smooth=3,
             method="medianvalues", filename=projectdir+"/0-6-windplot-windspeed-80min"+"-"+type)

    windplot(superFrameAugmented, "humidity_HLL_545", polar=False,
             useMedian=True, title="Humidity "+type, smooth=3,
             method="medianvalues", filename=projectdir+"/0-7-windplot-humidity-allhum"+"-"+type)

    simpleStripPlot(superFrameAugmented, x="windspeedcat", y="humidity_HLL_545",
                      xlim=(0, 15), ylim=(5, 100), title="Windspeed vs humidity "+type,
                      filename=projectdir+"/0-8-stripplot-windspeed-humidity-allhum"+"-"+type)




    return
    simpleStripPlot(superFrameAugmented, x="datehour", y="pm25_diff_545_NL",
                      xlim=(0, 24), ylim=(-20, 20), title="hour vs diff 545 - NL")

    simpleStripPlot(superFrameAugmented, x="datehour", y="humidity_HLL_545",
                      xlim=(0, 24), ylim=(10, 100), title="hour vs humidity")

    simpleStripPlot(superFrameAugmented, x="datehour", y="windspeed",
                      xlim=(0, 24), ylim=(0, 20), title="hour vs windspeed")

    simpleStripPlot(superFrameAugmented, x="datehour", y="pm25_NL49570",
                      xlim=(0, 24), ylim=(-10, 60), title="hour vs pm25")

    simpleStripPlot(superFrameAugmented, x="dateday", y="pm25_diff_545_NL",
                      xlim=(-1, 7), ylim=(-20, 20), title="day vs diff 545 - NL",
                    xfont=10)

    simpleStripPlot(superFrameAugmented, x="dateday", y="humidity_HLL_545",
                      xlim=(-1, 7), ylim=(10, 100), title="day vs humidity",
                    xfont=10)

    simpleStripPlot(superFrameAugmented, x="dateday", y="windspeed",
                      xlim=(-1, 7), ylim=(0, 20), title="day vs windspeed",
                    xfont=10)

    simpleStripPlot(superFrameAugmented, x="dateday", y="pm25_NL49570",
                      xlim=(-1, 7), ylim=(-10, 60), title="day vs pm25",
                    xfont=10)

    simpleStripPlot(superFrameAugmented, x="windspeedcat", y="pm25_diff_545_NL",
                      xlim=(0, 15), ylim=(-10, 20), title="Windspeed vs diff 545 - NL")

    return
#    diffPlotSensors(superFrameAugmented, "pm25", allSensorsText, projectdir + "/diffplots-sensors")

#    diffWindPlotSensors(superFrameAugmented, "pm25", allSensorsText, projectdir + "/windplots-sensors", smooth=3)
    windplot(superFrameAugmented, "pm25_diff_545_549", polar=False,
             method="meanvalues", smooth=3, title="windplot mean 545 - 549")

    windplot(superFrameAugmented, "pm25_diff_545_549", polar=False,
             method="medianvalues", smooth=3, title="windplot median 545 - 549")

    windplot(superFrameAugmented, "pm25_diff_545_NL", polar=False,
             method="meanvalues", smooth=3, title="windplot mean 545 - NL")

    windplot(superFrameAugmented, "pm25_diff_545_NL", polar=False,
             method="medianvalues", smooth=3, title="windplot median 545 - NL")

    simpleStripPlot(superFrameAugmented, x="windspeedcat", y="pm25_diff_545_NL",
                      xlim=(0, 15), ylim=(-10, 20), title="Windspeed vs diff 545 - NL")

    simpleStripPlot(superFrameAugmented, x="windspeedcat", y="humidity_HLL_545",
                      xlim=(0, 15), ylim=(10, 100), title="Windspeed vs humidity 545")

    simpleStripPlot(superFrameAugmented, x="windspeedcat", y="winddirection",
                      xlim=(0, 15), ylim=(5, 365), title="Windspeed vs winddirection")

    simpleStripPlot(superFrameAugmented, x="humiditycat", y="pm25_diff_545_NL",
                     xlim=(0, 10), ylim=(-10, 20), title="Humidity vs diff 545 - NL")

    return
    simpleStripPlot(superFrameAugmented, xlim=(0,36), ylim=(-5,30),
                    x="winddirection", y="pm25_NL49570", jitter=0.6)

    # superFrameAugmented = superFrameAugmented[superFrameAugmented["humidity_HLL_545"] < 81]

    simpleScatterPlot(superFrameAugmented, "temperature_HLL_549", "temperature_knmi",
                      xlim=(-10,40), ylim=(-10,40))

#    superFrameAugmented = superFrameAugmented[superFrameAugmented["windspeed"] > 4]

#    superFrameAugmented = superFrameAugmented[superFrameAugmented["windspeed"] < 4]

    simpleStripPlot(superFrameAugmented, xlim=(0,20), ylim=(0,3),x="windspeed", y="quotient")
#    superFrameAugmented = superFrameAugmented[superFrameAugmented["windspeed"] > 12]
    attrPlot(superFrameAugmented, "pm25_diff_545_NL", binwidth=0.5)

    simpleStripPlot(superFrameAugmented, xlim=(0,20), ylim=(20,100),x="windspeed", y="humidity_HLL_545")

    windplot(superFrameAugmented, "pm25_NL49570", polar=False,
             useMedian=True, title="PM25 NL49570", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-NL49570")

    windplot(superFrameAugmented, "pm25_HLL_545", polar=False,
             useMedian=True, title="PM25 HLL 545", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-545")

    windplot(superFrameAugmented, "pm25_diff_545_NL", polar=False,
             useMedian=True, title="PM25 difference 545 - NL", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-545-NL")

    windplot(superFrameAugmented, "pm25_OZK_1845", polar=False,
             useMedian=True, title="PM25 OZK 1845", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-1845")

    windplot(superFrameAugmented, "pm25_diff_1845_NL", polar=False,
             useMedian=True, title="PM25 difference 1845 - NL", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-1845-NL")

    windplot(superFrameAugmented, "windspeed", polar=False,
             useMedian=True, title="Windspeed", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-windspeed")

    windplot(superFrameAugmented, "humidity_HLL_545", polar=False,
             useMedian=True, title="Humidity 545", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-humidity_545")

    windplot(superFrameAugmented, "temperature_HLL_545", polar=False,
             useMedian=True, title="Temperature 545", smooth=3,
             method="medianvalues", filename=projectdir+"/6-windplot-temperature_545")

    return

    windplot(superFrameAugmented, "pm25_diff_545_549", polar=False,
             useMedian=True, title="PM25 difference 545 - 549", smooth=3,
             method="medianvalues", filename=projectdir+"/4-windplot-545-549")

    diffPlot(HLL_545, HLL_549, attr="pm25", title="Difference 545 vs 549", xlim=(-2.5, 2.5),
             filename=projectdir+"/1-HLL-diffplot", binwidth=0.1)

    simpleJointPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_545",
                      xlim=(-5, 40), ylim=(-5, 40), title="Scatterplot NL - 545",
                      filename=projectdir+"/scatter-NL-545", dotsize=60, hue="highhumidity")

    simpleScatterPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_545",
                      xlim=(-5, 25), ylim=(-5, 25), title="Scatterplot NL - 545 (detail)",
                      filename=projectdir+"/scatter-NL-545", dotsize=20)

    simpleScatterPlot(superFrameAugmented, x="humidity_HLL_545", y="pm25_HLL_545",
                      xlim=(0, 100), ylim=(-10, 125), title="Humidity 545 vs pm25 545",
                      filename=projectdir+"/5-humidity-pm25-545")

    simpleScatterPlot(superFrameAugmented, x="humidity_HLL_545", y="pm25_NL49570",
                      xlim=(0, 100), ylim=(-10, 125), title="Humidity 545 vs pm25 NL",
                      filename=projectdir+"/5-humidity-pm25-NL")

    simpleScatterPlot(superFrameAugmented, x="humidity_HLL_545", y="pm25_OZK_1845",
                      xlim=(0, 100), ylim=(-10, 125), title="Humidity 545 vs pm25 1845",
                      filename=projectdir+"/5-humidity-pm25-1845")

    simpleScatterPlot(superFrameAugmented, x="humidity_OZK_1845", y="pm25_OZK_1845",
                      xlim=(0, 100), ylim=(-10, 125), title="Humidity 1845 vs pm25 1845",
                      filename=projectdir+"/5-humidity-pm25-1845")

    simpleJointPlot(superFrameAugmented, x="humidity_OZK_1845", y="humidity_HLL_545",
                      xlim=(0, 100), ylim=(0, 100), title="Humidity 1845 vs humidity 545",
                      filename=projectdir+"/5-humidity-1845-humidity-545", dotsize=10)


    simpleJointPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_545",
                      xlim=(-5, 40), ylim=(-5, 40), title="Scatterplot NL - 545",
                      filename=projectdir+"/scatter-NL-545", dotsize=60, hue="highhumidity")

    diffPlot(HLL_545, HLL_549, attr="pm25", title="Difference 545 vs 549", xlim=(-2.5, 2.5),
             filename=projectdir+"/1-HLL-diffplot")

    superFrameAugmented=superFrameAugmented[superFrameAugmented["humidity_HLL_545"] < 80.0]

    simpleJointPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_545",
                      xlim=(-5, 40), ylim=(-5, 40), title="Scatterplot NL - 545, humidity < 80",
                      filename=projectdir+"/scatter-NL-545-humidityless80", dotsize=20)

    HLL_545 = HLL_545[HLL_545["humidity"] < 80]
    HLL_549 = HLL_549[HLL_549["humidity"] < 80]

    diffPlot(HLL_545, HLL_549, attr="pm25", title="Difference 545 vs 549 humidity < 80", xlim=(-2.5, 2.5),
             filename=projectdir + "/1-HLL-diffplot-humidityless80")

    return
    simpleScatterPlot(superFrameAugmented, x="humidity_HLL_545", y="pm25_diff_545_NL",
                      xlim=(0, 100), ylim=(-80, 80), title="Humidity 545 vs Diff pm25 545",
                      filename=projectdir+"/5-humidity-pm25-diff-545")

    simpleScatterPlot(superFrameAugmented, x="humidity_HLL_545", y="pm25_OZK_1845",
                      xlim=(0, 100), ylim=(-10, 125), title="Humidity 545 vs pm25 1845",
                      filename=projectdir+"/5-humidity-pm25-1845")


    simpleScatterPlot(superFrameAugmented, x="humidity_OZK_1845", y="pm25_OZK_1845",
                      xlim=(0, 100), ylim=(-10, 125), title="Humidity 1845 vs pm25 1845",
                      filename=projectdir+"/5-humidity-pm25-1845")

    simpleScatterPlot(superFrameAugmented, x="humidity_OZK_1845", y="humidity_HLL_545",
                      xlim=(0, 100), ylim=(-10, 125), title="Humidity 1845 vs humidity 545",
                      filename=projectdir+"/5-humidity-1845-humidity-545")

    simpleJointPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_545",
                      xlim=(-10, 50), ylim=(-20, 40), title="LML Absolute vs 545",
                      filename=projectdir+"/3-49570-545", )


#    setPlotSizeLandscape()
#    lplot = sns.catplot(s=1, data=superFrameAugmented, kind="swarm", x="windspeed",
#                        y="pm25_diff_545_NL")
#    lplot.set(xlim=(0, 25))
#    lplot.set(ylim=(-50, 50))

    simpleStripPlot(superFrameAugmented, x="windspeed", y="pm25_diff_545_NL",
                      xlim=(0, 20), ylim=(-25, 25), title="Windspeed vs difference 545 - NL",
                      filename=projectdir+"/4-windspeed-545-NL")

    simpleStripPlot(superFrameAugmented, x="windspeed", y="temperature_HLL_545",
                      xlim=(0, 20), ylim=(0, 40), title="Windspeed vs temperature 545",
                      filename=projectdir+"/4-windspeed-temperature-545")

    simpleStripPlot(superFrameAugmented, x="windspeed", y="humidity_HLL_545",
                      xlim=(0, 20), ylim=(20, 100), title="Windspeed vs humidity 545",
                      filename=projectdir+"/4-windspeed-humidity-545")

    simpleStripPlot(superFrameAugmented, x="windspeed", y="pm25_NL49570",
                      xlim=(0, 20), ylim=(-10, 50), title="Windspeed vs pm25 NL",
                      filename=projectdir+"/4-windspeed-pm25-NL")


    windplot(superFrameAugmented, "pm25_diff_545_NL", polar=False,
             useMedian=True, title="PM25 difference 545 - LML", smooth=3,
             method="medianvalues", filename=projectdir+"/4-windplot-545-NL")

    windplot(superFrameAugmented, "pm25_diff_549_NL", polar=False,
             useMedian=True, title="PM25 difference 549 - LML", smooth=3,
             method="medianvalues", filename=projectdir+"/4-windplot-549-NL")

    windplot(superFrameAugmented, "pm25_diff_1845_NL", polar=False,
             useMedian=True, title="PM25 difference 1845 - LML", smooth=3,
             method="medianvalues", filename=projectdir+"/4-windplot-1845-NL")

    windplot(superFrameAugmented, "pm25_diff_545_549", polar=False,
             useMedian=True, title="PM25 difference 545 - 549", smooth=3,
             method="medianvalues", filename=projectdir+"/4-windplot-545-549")

    simpleScatterPlot(superFrameAugmented, x="windspeed", y="pm25_diff_545_549",
                      xlim=(0, 30), ylim=(-50, 80), title="Windspeed vs difference 545 - 549",
                      filename=projectdir+"/4`-windspeed-545-549")


#    attrPlot(superFrameAugmented, "pm25_diff_545_NL", binwidth=0.25, xlim=(-20, 60), describe=True)
#    attrPlot(superFrameAugmented, "pm25_diff_549_NL", binwidth=0.25, xlim=(-20, 60))
#    attrPlot(superFrameAugmented, "pm25_diff_1845_NL", binwidth=0.25, xlim=(-20, 60))
#    attrPlot(superFrameAugmented, "pm25_diff_1850_NL", binwidth=0.25, xlim=(-20, 60))

    diffPlot(HLL_545, HLL_549, attr="pm25", title="Difference 545 vs 549", xlim=(-2.5, 2.5),
             filename=projectdir+"/1-HLL-diffplot")
    diffPlot(OZK_1845, OZK_1850, attr="pm25", title="Difference 1845 vs 1850", xlim=(-2.5, 2.5),
             filename=projectdir+"/1-OZK-diffplot")
    diffPlot(HLL_545, NL49570, attr="pm25", title="Difference 545 vs LML", xlim=(-20, 20),
             filename=projectdir+"/2-545-NL-diffplot")
    diffPlot(HLL_549, NL49570, attr="pm25", title="Difference 549 vs LML", xlim=(-20, 20),
             filename=projectdir+"/2-549-NL-diffplot")
    diffPlot(OZK_1845, NL49570, attr="pm25", title="Difference 1845 vs LML", xlim=(-20, 20),
             filename=projectdir+"/2-1845-NL-diffplot")
    diffPlot(OZK_1850, NL49570, attr="pm25", title="Difference 1850 vs LML", xlim=(-20, 20),
             filename=projectdir+"/2-1849-NL-diffplot")

    simpleScatterPlot(superFrameAugmented, x="windspeed", y="pm25_diff_545_NL",
                      xlim=(0, 30), ylim=(-50, 80), title="Windspeed vs difference 545-LML",
                      filename=projectdir+"/3-windspeed-545Diff")

    simpleScatterPlot(superFrameAugmented, x="windspeed", y="pm25_diff_549_NL",
                      xlim=(0, 30), ylim=(-50, 80), title="Windspeed vs difference 549-LML",
                      filename=projectdir+"/3-windspeed-545Diff")

    simpleScatterPlot(superFrameAugmented, x="windspeed", y="pm25_diff_1845_NL",
                      xlim=(0, 30), ylim=(-50, 80), title="Windspeed vs difference 1845-LML",
                      filename=projectdir+"/3-windspeed-1845Diff")
    simpleScatterPlot(superFrameAugmented, x="windspeed", y="pm25_NL49570",
                      xlim=(0, 30), ylim=(-10, 75), title="Windspeed vs LML Absolute",
                      filename=projectdir+"/3-windspeed-49570")
    simpleScatterPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_diff_545_NL",
                      xlim=(-10, 50), ylim=(-20, 40), title="LML Absolute vs diff545",
                      filename=projectdir+"/3-49570-Diff545", )
    simpleScatterPlot(superFrameAugmented, x="pm25_NL49570", y="pm25_HLL_545",
                      xlim=(-10, 50), ylim=(-20, 40), title="LML Absolute vs 545",
                      filename=projectdir+"/3-49570-545", )

#    diffPlot(HLL_545, OZK_1850, attr="pm25", title="Difference 545 vs 1850", xlim=(-10, 10))
#    diffPlot(HLL_549, OZK_1850, attr="pm25", title="Difference 549 vs 1850", xlim=(-10, 10))
#    diffPlot(HLL_545, OZK_1845, attr="pm25", title="Difference 545 vs 1845", xlim=(-10, 10))
#   diffPlot(HLL_549, OZK_1845, attr="pm25", title="Difference 549 vs 1845", xlim=(-10, 10))


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



