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
NL10418 = pd.DataFrame()
HLL_469 = pd.DataFrame()
HLL_506 = pd.DataFrame()
NL49704 = pd.DataFrame()
HLL_323 = pd.DataFrame()
HLL_527 = pd.DataFrame()
NL49551 = pd.DataFrame()
HLL_509 = pd.DataFrame()
HLL_546 = pd.DataFrame()
HLL_284 = pd.DataFrame()
NL49701 = pd.DataFrame()
NL49573 = pd.DataFrame()
NL49561 = pd.DataFrame()
HLL_298 = pd.DataFrame()
locations = pd.DataFrame()
NL10404 = pd.DataFrame()
HLL_350 = pd.DataFrame()
HLL_415 = pd.DataFrame()
NL10636 = pd.DataFrame()
HLL_462 = pd.DataFrame()
HLL_474 = pd.DataFrame()
NL10738 = pd.DataFrame()
HLL_439 = pd.DataFrame()
HLL_413 = pd.DataFrame()
NL10538 = pd.DataFrame()
NL10641 = pd.DataFrame()
NL49570 = pd.DataFrame()
HLL_532 = pd.DataFrame()
NL49017 = pd.DataFrame()
HLL_448 = pd.DataFrame()
HLL_334 = pd.DataFrame()
NL49556 = pd.DataFrame()
HLL_458 = pd.DataFrame()
HLL_250 = pd.DataFrame()
startdate = "20230908"
enddate = "20230909"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/smog-20230908"
sensorList = ["NL10644", "NL10418", "HLL_469", "HLL_506", "NL49704", "HLL_323", "HLL_527", "NL49551", "HLL_509", "HLL_546", "HLL_284", "NL49701", "NL49573", "NL49561", "HLL_298", "NL10404", "HLL_350", "HLL_415", "NL10636", "HLL_462", "HLL_474", "NL10738", "HLL_439", "HLL_413", "NL10538", "NL10641", "NL49570", "HLL_532", "NL49017", "HLL_448", "HLL_334", "NL49556", "HLL_458", "HLL_250"]
sensorListNL = ["NL10644", "NL10418", "NL49704", "NL49551", "NL49701", "NL49573", "NL49561",
                "NL10404", "NL10636", "NL10738", "NL10538", "NL10641", "NL49570", "NL49017",
                "NL49556"]

def convertTextToDataFrame(aText):
    return globals()[aText]

# size with quadratic value
def getsize(value, factor):
    if value > 100:
        value = 100
    size = math.floor((value + 10) / 10)
    return size * factor

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

    fig = px.scatter_mapbox(snapshots, lat='lat', lon='lon', color='pm25',
                            center=dict(lat=52.471, lon=4.810),
                            zoom=8,
                            # mapbox_style = 'open-street-map',
                            mapbox_style='carto-darkmatter',
                            range_color=(1, 100),
                            opacity=0.9,
                            size="pm25",
                            size_max=50,
                            animation_frame="time",
                            animation_group="time"
    )

    fig.write_html("export.html")
    fig.show()

    printf("Done\n")
    return


# run stand alone entry point
if __name__ == '__main__':
  #  printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



