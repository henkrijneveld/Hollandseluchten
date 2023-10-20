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

# import cv2 library
import cv2

# General
wideFrame = pd.DataFrame()
wideFrameAugmented = pd.DataFrame()
HLL_298 = pd.DataFrame()
HLL_345 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
NL49701 = pd.DataFrame()
NL49556 = pd.DataFrame()
HLL_256 = pd.DataFrame()
HLL_307 = pd.DataFrame()
HLL_320 = pd.DataFrame()
HLL_531 = pd.DataFrame()
startdate = "20230101"
enddate = "20231001"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/verkeer-20231019"
allSensorsList = ["HLL_298", "HLL_345", "KNMI_240", "NL49701", "NL49556",
                  "HLL_256", "HLL_307", "HLL_320", "HLL_531"]
sensorList = ["NL49701", "NL49556", "HLL_345", "HLL_307", "HLL_298", "HLL_320", "HLL_531"]

mergetype="outer"

def getMergetype():
    global mergetype
    return mergetype

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
    global HLL_345

    HLL_345 = HLL_345[HLL_345["pm25"] < 200]

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


def highhumidity(aRow):
    humidity = aRow["humidity_HLL_298"]
    return humidity > 80

# add columns:
#
# write result to superFrameAugmented.csv
def augmentWideFrame(sensorList):
    global wideFrame
    global wideFrameAugmented

    # create all the diff columns
    printf("Building diff columns: ")
    for baselist in sensorList:
        for comparelist in sensorList:
            createDiffColumn(wideFrame, "pm25_" + baselist, "pm25_" + comparelist,
                             "pm25_diff_" + baselist + "_" + comparelist)
            printf(">")
    printf("\n")

#    wideFrame["highhumidity"] = wideFrame.apply(highhumidity, axis=1)

    wideFrame["highhumidity"] = wideFrame["humidity_HLL_298"] > 80
#    wideFrame = wideFrame[wideFrame["humidity_HLL_298"] < 80]

    wideFrame['datehour'] = wideFrame['datetime'].dt.hour
    wideFrame['dateday'] = wideFrame['datetime'].dt.day_name()  # monday = 0

    wideFrameAugmented = wideFrame.copy()
    wideFrameAugmented.to_csv(projectdir + "/wideFrameAugmented.csv", index=False)

    return wideFrameAugmented


def runit():
    global wideFrame
    global wideFrameAugmented

    allSensors = convertTextToDataFrame(sensorList)
#    createTimeSeries_Multiple(list(zip(allSensors, sensorList)), projectdir, namesuffix="pm25",
#                              fname="timeseries-sensors")
    createWideFrame(allSensorsList, KNMI_240)
    augmentWideFrame(sensorList)

    # print dagelijkse gang
#    for sensor in sensorList:
#        simpleStripPlot(wideFrame, "datehour", "pm25_" + sensor, xlim=(-1,24), ylim=(0,40),
#                        title=sensor + " dagelijkse gang", xfont=11,
#                        filename=projectdir+"/gang-"+sensor)

    # print all diff plots
#    printf("Diffplots: ")
#    for baselist in sensorList:
#        for comparelist in sensorList:
#            simpleStripPlot(wideFrame, "datehour", "pm25_" + sensor,
#                            xlim=(-1, 24), ylim=(-7, 7),
#                            title=baselist + " - " + comparelist + " delta pm25", xfont=11,
#                            filename=projectdir+"/diff-"+baselist+"-"+comparelist)
#            printf(">")
#    printf("\n")

    # read the images
#    printf("Concat images: ")
#    rows = []
#    for baselist in sensorList:
#        rowList = []
#        for comparelist in sensorList:
#            filename = "/diff-"+baselist+"-"+comparelist+".png"
#            img = cv2.imread(projectdir + "/" + filename)
#            rowList.append(img)
#            printf(">")
#        rowimg = cv2.hconcat(rowList)
#        rows.append(rowimg)
#    totalimg = cv2.vconcat(rows)
#    printf("\n")
#    cv2.imwrite(projectdir+"/totaldiffs.jpg", totalimg, [int(cv2.IMWRITE_JPEG_QUALITY), 85])

    # print all diff plots
    printf("Diffplots median: ")
    for baselist in sensorList:
        for comparelist in sensorList:
            plotframe = medianvalues([wideFrameAugmented], "datehour", "pm25_diff_" + baselist + "_" + comparelist)
#            simpleStripPlot(wideFrame, "datehour", "pm25_diff_" + baselist + "_" + comparelist,
#                            xlim=(-1, 24), ylim=(-7, 7),
#                            title=baselist + " - " + comparelist + " delta pm25", xfont=11,
#                            filename=projectdir+"/diff-median-"+baselist+"-"+comparelist)
            lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_diff_" + baselist + "_" + comparelist, linewidth=2.5))
            lplot.set(xlim=(-1, 24))
            lplot.set(title=baselist + " - " + comparelist + " delta pm25")
            lplot.set_ylabel("Difference median", fontsize=14)
            lplot.set_xlabel("Hour of day (UTC)", fontsize=14)

            plt.tight_layout()
            lplot.get_figure().savefig(projectdir+"/diff-median-"+baselist+"-"+comparelist)
            plt.close()
            printf(">")
    printf("\n")

    # read the images
    printf("Concat images: ")
    rows = []
    for baselist in sensorList:
        rowList = []
        for comparelist in sensorList:
            filename = "/diff-median-"+baselist+"-"+comparelist+".png"
            img = cv2.imread(projectdir + "/" + filename)
            rowList.append(img)
            printf(">")
        rowimg = cv2.hconcat(rowList)
        rows.append(rowimg)
    totalimg = cv2.vconcat(rows)
    printf("\n")
    cv2.imwrite(projectdir+"/totaldiffs-median.jpg", totalimg, [int(cv2.IMWRITE_JPEG_QUALITY), 85])

    # print all diff plots
    printf("Diffplots mean: ")
    for baselist in sensorList:
        for comparelist in sensorList:
            plotframe = meanvalues([wideFrameAugmented], "datehour", "pm25_diff_" + baselist + "_" + comparelist)
            #            simpleStripPlot(wideFrame, "datehour", "pm25_diff_" + baselist + "_" + comparelist,
            #                            xlim=(-1, 24), ylim=(-7, 7),
            #                            title=baselist + " - " + comparelist + " delta pm25", xfont=11,
            #                            filename=projectdir+"/diff-median-"+baselist+"-"+comparelist)
            lplot = (sns.lineplot(data=plotframe, x="datehour", y="pm25_diff_" + baselist + "_" + comparelist,
                                  linewidth=2.5))
            lplot.set(xlim=(-1, 24))
            lplot.set(title=baselist + " - " + comparelist + " delta pm25")
            lplot.set_ylabel("Difference mean", fontsize=14)
            lplot.set_xlabel("Hour of day (UTC)", fontsize=14)

            plt.tight_layout()
            lplot.get_figure().savefig(projectdir + "/diff-mean-" + baselist + "-" + comparelist)
            plt.close()
            printf(">")
    printf("\n")

    # read the images
    printf("Concat images: ")
    rows = []
    for baselist in sensorList:
        rowList = []
        for comparelist in sensorList:
            filename = "/diff-mean-" + baselist + "-" + comparelist + ".png"
            img = cv2.imread(projectdir + "/" + filename)
            rowList.append(img)
            printf(">")
        rowimg = cv2.hconcat(rowList)
        rows.append(rowimg)
    totalimg = cv2.vconcat(rows)
    printf("\n")
    cv2.imwrite(projectdir + "/totaldiffs-mean.jpg", totalimg, [int(cv2.IMWRITE_JPEG_QUALITY), 85])

    return

# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



