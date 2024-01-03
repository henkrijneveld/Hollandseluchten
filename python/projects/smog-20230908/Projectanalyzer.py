# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

# STAARTEN, WINDPUFJES EN GOUDEN STANDAARDS

import sys
sys.path.insert(0, '../..')
from analyzer import *
from plotter import *
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"

import math
import pprint as pp


# General
NL10644 = pd.DataFrame()
NL01496 = pd.DataFrame()
NL10418 = pd.DataFrame()
# Warning: NL10448.csv could not be read, skipped
NL10247 = pd.DataFrame()
NL49704 = pd.DataFrame()
NL49551 = pd.DataFrame()
NL10938 = pd.DataFrame()
NL01913 = pd.DataFrame()
NL49557 = pd.DataFrame()
NL49701 = pd.DataFrame()
NL01495 = pd.DataFrame()
NL49573 = pd.DataFrame()
NL49561 = pd.DataFrame()
NL10450 = pd.DataFrame()
NL01494 = pd.DataFrame()
locations = pd.DataFrame()
NL10404 = pd.DataFrame()
NL01488 = pd.DataFrame()
NL10449 = pd.DataFrame()
NL49553 = pd.DataFrame()
NL10131 = pd.DataFrame()
NL10934 = pd.DataFrame()
NL10248 = pd.DataFrame()
# Warning: NL10136.csv could not be read, skipped
NL49572 = pd.DataFrame()
NL01487 = pd.DataFrame()
NL01912 = pd.DataFrame()
NL10444 = pd.DataFrame()
NL10643 = pd.DataFrame()
NL10636 = pd.DataFrame()
NL10230 = pd.DataFrame()
NL10738 = pd.DataFrame()
NL10741 = pd.DataFrame()
NL10742 = pd.DataFrame()
NL10138 = pd.DataFrame()
NL01485 = pd.DataFrame()
NL53001 = pd.DataFrame()
NL10241 = pd.DataFrame()
NL49012 = pd.DataFrame()
NL10821 = pd.DataFrame()
NL10240 = pd.DataFrame()
NL49007 = pd.DataFrame()
NL10937 = pd.DataFrame()
NL10538 = pd.DataFrame()
NL10641 = pd.DataFrame()
NL49570 = pd.DataFrame()
NL49017 = pd.DataFrame()
NL49014 = pd.DataFrame()
NL53004 = pd.DataFrame()
NL01491 = pd.DataFrame()
NL49703 = pd.DataFrame()
NL49556 = pd.DataFrame()
NL01489 = pd.DataFrame()
NL49016 = pd.DataFrame()
startdate = "20231231"
enddate = "20240101"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/smog-20230908"
sensorList = ["NL10644", "NL01496", "NL10418", "NL10247", "NL49704", "NL49551", "NL10938", "NL01913", "NL49557", "NL49701", "NL01495", "NL49573", "NL49561", "NL10450", "NL01494", "NL10404", "NL01488", "NL10449", "NL49553", "NL10131", "NL10934", "NL10248", "NL49572", "NL01487", "NL01912", "NL10444", "NL10643", "NL10636", "NL10230", "NL10738", "NL10741", "NL10742", "NL10138", "NL01485", "NL53001", "NL10241", "NL49012", "NL10821", "NL10240", "NL49007", "NL10937", "NL10538", "NL10641", "NL49570", "NL49017", "NL49014", "NL53004", "NL01491", "NL49703", "NL49556", "NL01489", "NL49016"]
sensorListNL = ["NL10644", "NL01496", "NL10418", "NL10247", "NL49704", "NL49551", "NL10938", "NL01913", "NL49557", "NL49701", "NL01495", "NL49573", "NL49561", "NL10450", "NL01494", "NL10404", "NL01488", "NL10449", "NL49553", "NL10131", "NL10934", "NL10248", "NL49572", "NL01487", "NL01912", "NL10444", "NL10643", "NL10636", "NL10230", "NL10738", "NL10741", "NL10742", "NL10138", "NL01485", "NL53001", "NL10241", "NL49012", "NL10821", "NL10240", "NL49007", "NL10937", "NL10538", "NL10641", "NL49570", "NL49017", "NL49014", "NL53004", "NL01491", "NL49703", "NL49556", "NL01489", "NL49016"]
sensorListHLL = []

def convertTextToDataFrame(aText):
    return globals()[aText]

# size with quadratic value
def getsize(value, factor):
    if value > 100:
        value = 100
    size = math.floor((value + 10) / 10)
    return size * factor

def getMaxVal(sensorlist, attr):
    maxval = 0
    for sensor in sensorlist:
        sensorFrame = convertTextToDataFrame(sensor)
        maxsensor = sensorFrame[attr].values.max()
        if maxsensor > maxval:
            maxval = maxsensor
    return maxval

# sensorlist: text
# start, string: yyyymmdd
# end, string: yyyymmdd
def makeSnapshots(sensorlist, start, end, locations):
    #@todo just an index, maybe later add a datetime somewhere
#    snapshots = []
    snapshots = None

    dt_start = convertToDatetime(start)
    dt_end = convertToDatetime(end)
    dt_end = dt_end + datetime.timedelta(days=1)
    while dt_start < dt_end:
        printf("%s\n", dt_start.strftime("%Y-%m-%d %H:%M:%S+00:00"))
        aDate = pd.to_datetime(dt_start.strftime("%Y-%m-%d %H:%M:%S+00:00"), utc=True)
#        aDate = dt_start.strftime("%Y-%m-%d %H:%M:%S+00:00")

        # could also copy locations, but this seems more flexible
        snapshot = pd.DataFrame(columns=["sensor", "time", "lat", "lon", "pm25", "size"])
        for sensorname in sensorlist:
            if sensorname in locations['sensor'].values:
                lat = locations.loc[locations['sensor'] == sensorname, "lat"].values[0]
                lon = locations.loc[locations['sensor'] == sensorname, "lon"].values[0]
                sensorframe = convertTextToDataFrame(sensorname)
                if sensorframe.shape[0] > 0:
                    if aDate in sensorframe["datetime"].values or True: #@todo Clear this datetime shit!
                        aSeries = sensorframe.loc[sensorframe["datetime"] == aDate, "pm25"]
                        if len(aSeries) > 0:
                            pm25 = aSeries.values[0]
                            if pm25 < 0:
                                pm25 = 0
                        else:
                            pm25 = 0
                        snapshot.loc[len(snapshot)] = [sensorname, dt_start.strftime("%Y-%m-%d %Hh"), lat, lon, pm25, getsize(pm25, 2)]
#        if snapshot.shape[0] > 0:
#            snapshots.append(snapshot)
        if snapshots is None:
            snapshots = snapshot.copy()
        else:
            snapshots = pd.concat([snapshots, snapshot])
        dt_start = dt_start + datetime.timedelta(hours=1)
    return snapshots

def runit():
    snapshots = makeSnapshots(sensorListNL, startdate, enddate, locations)

    maxpm25 = getMaxVal(sensorListNL, "pm25")
    maxpm25 = 5 * (int((maxpm25 + 5) / 5))
    if maxpm25 > 150:
        maxpm25 = 150

    fig = px.scatter_mapbox(snapshots, lat='lat', lon='lon', color='pm25',
                            center=dict(lat=52.471, lon=4.810),
                            zoom=7,
                            # mapbox_style = 'open-street-map',
                            mapbox_style='carto-darkmatter',
                            range_color=(1, maxpm25),
                            opacity=0.9,
                            size="pm25",
                            size_max=20,
                            animation_frame="time",
                            animation_group="time"
    )

    fig.write_html("exportNL.html")
    fig.show()

    printf("Done\n")
    return


# run stand alone entry point
if __name__ == '__main__':
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



