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

HLL_298 = pd.DataFrame()
HLL_462 = pd.DataFrame()
HLL_323 = pd.DataFrame()
HLL_532 = pd.DataFrame()
NL49570 = pd.DataFrame()
NL49701 = pd.DataFrame()
HLL_284 = pd.DataFrame()
KNMI_225 = pd.DataFrame()
locations = pd.DataFrame()
HLL_527 = pd.DataFrame()
HLL_413 = pd.DataFrame()
startdate = "20230908"
enddate = "20230909"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/smog-20230908"
sensorList = ["HLL_298", "HLL_462", "HLL_323", "HLL_532", "NL49570", "NL49701", "HLL_284", "KNMI_225", "HLL_527", "HLL_413"]

# General

def convertTextToDataFrame(aText):
    return globals()[aText]

# sensorlist: text
# start, string: yyyymmdd
# end, string: yyyymmdd
def makeSnapshots(sensorlist, start, end):
    #@todo just an index, maybe later add a datetime somewhere
    snapshots = []
    dt_start = convertToDatetime(start)
    dt_end = convertToDatetime(end)
    dt_end = dt_end + datetime.timedelta(days=1)
    while dt_start < dt_end:
        printf("%s\n", dt_start.strftime("%Y-%m-%d %H:%M:%S+00:00"))
        aDate = pd.to_datetime(dt_start.strftime("%Y-%m-%d %H:%M:%S+00:00"))
#        aDate = dt_start.strftime("%Y-%m-%d %H:%M:%S+00:00")

        # could also copy locations, but this seems more flexible
        snapshot = pd.DataFrame(columns=["sensor", "lat", "lon", "pm25"])
        for sensorname in sensorlist:
            if sensorname in locations['sensor'].values:
                lat = locations.loc[locations['sensor'] == sensorname, "lat"].values[0]
                lon = locations.loc[locations['sensor'] == sensorname, "lon"].values[0]
                sensorframe = convertTextToDataFrame(sensorname)
                tmp = sensorframe["datetime"].values
                if aDate in sensorframe["datetime"].values:
                    pm25 = sensorframe.loc[sensorframe["datetime"] == aDate]["pm25"]
                    snapshot.loc[len(snapshot)] = [sensorname, lat, lon, pm25]
        if snapshot.shape[0] > 0:
            snapshots.append(snapshot)
        dt_start = dt_start + datetime.timedelta(hours=1)
    return snapshots

def runit():
    snapshots = makeSnapshots(sensorList, startdate, enddate)
    return


# run stand alone entry point
if __name__ == '__main__':
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



