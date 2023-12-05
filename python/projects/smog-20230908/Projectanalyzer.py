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
NL10742 = pd.DataFrame()
HLL_261 = pd.DataFrame()
HLL_288 = pd.DataFrame()
HLL_426 = pd.DataFrame()
HLL_549 = pd.DataFrame()
NL49703 = pd.DataFrame()
HLL_324 = pd.DataFrame()
NL01912 = pd.DataFrame()
HLL_259 = pd.DataFrame()
HLL_275 = pd.DataFrame()
HLL_475 = pd.DataFrame()
NL01494 = pd.DataFrame()
HLL_543 = pd.DataFrame()
NL10131 = pd.DataFrame()
HLL_298 = pd.DataFrame()
HLL_300 = pd.DataFrame()
HLL_462 = pd.DataFrame()
HLL_280 = pd.DataFrame()
HLL_410 = pd.DataFrame()
NL49007 = pd.DataFrame()
HLL_295 = pd.DataFrame()
HLL_424 = pd.DataFrame()
HLL_513 = pd.DataFrame()
NL01495 = pd.DataFrame()
HLL_441 = pd.DataFrame()
HLL_542 = pd.DataFrame()
HLL_323 = pd.DataFrame()
HLL_452 = pd.DataFrame()
HLL_506 = pd.DataFrame()
HLL_427 = pd.DataFrame()
NL01491 = pd.DataFrame()
HLL_345 = pd.DataFrame()
NL10741 = pd.DataFrame()
NL10538 = pd.DataFrame()
NL49556 = pd.DataFrame()
HLL_365 = pd.DataFrame()
NL10821 = pd.DataFrame()
NL10934 = pd.DataFrame()
HLL_512 = pd.DataFrame()
HLL_247 = pd.DataFrame()
HLL_532 = pd.DataFrame()
HLL_326 = pd.DataFrame()
HLL_541 = pd.DataFrame()
HLL_250 = pd.DataFrame()
HLL_531 = pd.DataFrame()
HLL_444 = pd.DataFrame()
NL10644 = pd.DataFrame()
NL49017 = pd.DataFrame()
HLL_291 = pd.DataFrame()
HLL_501 = pd.DataFrame()
NL10241 = pd.DataFrame()
HLL_476 = pd.DataFrame()
HLL_442 = pd.DataFrame()
NL49014 = pd.DataFrame()
HLL_438 = pd.DataFrame()
HLL_443 = pd.DataFrame()
HLL_434 = pd.DataFrame()
HLL_546 = pd.DataFrame()
NL10240 = pd.DataFrame()
NL49570 = pd.DataFrame()
HLL_221 = pd.DataFrame()
HLL_505 = pd.DataFrame()
NL10248 = pd.DataFrame()
NL49701 = pd.DataFrame()
HLL_450 = pd.DataFrame()
HLL_329 = pd.DataFrame()
HLL_284 = pd.DataFrame()
HLL_301 = pd.DataFrame()
NL49557 = pd.DataFrame()
NL01496 = pd.DataFrame()
HLL_223 = pd.DataFrame()
HLL_224 = pd.DataFrame()
NL53004 = pd.DataFrame()
NL01485 = pd.DataFrame()
HLL_458 = pd.DataFrame()
NL53001 = pd.DataFrame()
HLL_547 = pd.DataFrame()
HLL_440 = pd.DataFrame()
HLL_321 = pd.DataFrame()
HLL_256 = pd.DataFrame()
HLL_538 = pd.DataFrame()
HLL_470 = pd.DataFrame()
NL10444 = pd.DataFrame()
HLL_509 = pd.DataFrame()
HLL_293 = pd.DataFrame()
# Warning: NL10448.csv could not be read, skipped
HLL_230 = pd.DataFrame()
HLL_474 = pd.DataFrame()
HLL_525 = pd.DataFrame()
NL49012 = pd.DataFrame()
HLL_453 = pd.DataFrame()
HLL_508 = pd.DataFrame()
HLL_235 = pd.DataFrame()
NL49553 = pd.DataFrame()
HLL_306 = pd.DataFrame()
NL10247 = pd.DataFrame()
HLL_315 = pd.DataFrame()
HLL_339 = pd.DataFrame()
HLL_533 = pd.DataFrame()
NL10641 = pd.DataFrame()
HLL_334 = pd.DataFrame()
NL10738 = pd.DataFrame()
HLL_332 = pd.DataFrame()
HLL_416 = pd.DataFrame()
HLL_341 = pd.DataFrame()
HLL_322 = pd.DataFrame()
HLL_350 = pd.DataFrame()
HLL_311 = pd.DataFrame()
HLL_330 = pd.DataFrame()
HLL_439 = pd.DataFrame()
HLL_278 = pd.DataFrame()
HLL_277 = pd.DataFrame()
locations = pd.DataFrame()
NL49704 = pd.DataFrame()
HLL_418 = pd.DataFrame()
HLL_245 = pd.DataFrame()
NL01913 = pd.DataFrame()
HLL_537 = pd.DataFrame()
HLL_420 = pd.DataFrame()
HLL_526 = pd.DataFrame()
HLL_465 = pd.DataFrame()
HLL_383 = pd.DataFrame()
HLL_313 = pd.DataFrame()
NL10138 = pd.DataFrame()
HLL_433 = pd.DataFrame()
HLL_415 = pd.DataFrame()
HLL_237 = pd.DataFrame()
HLL_519 = pd.DataFrame()
HLL_328 = pd.DataFrame()
HLL_226 = pd.DataFrame()
HLL_469 = pd.DataFrame()
HLL_527 = pd.DataFrame()
HLL_429 = pd.DataFrame()
HLL_319 = pd.DataFrame()
HLL_391 = pd.DataFrame()
NL49572 = pd.DataFrame()
NL10136 = pd.DataFrame()
HLL_307 = pd.DataFrame()
NL10404 = pd.DataFrame()
HLL_463 = pd.DataFrame()
HLL_281 = pd.DataFrame()
HLL_297 = pd.DataFrame()
HLL_344 = pd.DataFrame()
NL49016 = pd.DataFrame()
NL10643 = pd.DataFrame()
HLL_419 = pd.DataFrame()
HLL_320 = pd.DataFrame()
NL10636 = pd.DataFrame()
NL10449 = pd.DataFrame()
HLL_325 = pd.DataFrame()
HLL_240 = pd.DataFrame()
NL10418 = pd.DataFrame()
HLL_448 = pd.DataFrame()
NL01488 = pd.DataFrame()
HLL_528 = pd.DataFrame()
HLL_343 = pd.DataFrame()
HLL_333 = pd.DataFrame()
NL10450 = pd.DataFrame()
NL01487 = pd.DataFrame()
HLL_473 = pd.DataFrame()
HLL_511 = pd.DataFrame()
NL49573 = pd.DataFrame()
HLL_545 = pd.DataFrame()
HLL_363 = pd.DataFrame()
NL10938 = pd.DataFrame()
NL10230 = pd.DataFrame()
NL49551 = pd.DataFrame()
NL10937 = pd.DataFrame()
NL01489 = pd.DataFrame()
HLL_430 = pd.DataFrame()
NL49561 = pd.DataFrame()
HLL_413 = pd.DataFrame()
startdate = "20230908"
enddate = "20230909"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/smog-20230908"
sensorList = ["NL10742", "HLL_261", "HLL_288", "HLL_426", "HLL_549", "NL49703", "HLL_324", "NL01912", "HLL_259", "HLL_275", "HLL_475", "NL01494", "HLL_543", "NL10131", "HLL_298", "HLL_300", "HLL_462", "HLL_280", "HLL_410", "NL49007", "HLL_295", "HLL_424", "HLL_513", "NL01495", "HLL_441", "HLL_542", "HLL_323", "HLL_452", "HLL_506", "HLL_427", "NL01491", "HLL_345", "NL10741", "NL10538", "NL49556", "HLL_365", "NL10821", "NL10934", "HLL_512", "HLL_247", "HLL_532", "HLL_326", "HLL_541", "HLL_250", "HLL_531", "HLL_444", "NL10644", "NL49017", "HLL_291", "HLL_501", "NL10241", "HLL_476", "HLL_442", "NL49014", "HLL_438", "HLL_443", "HLL_434", "HLL_546", "NL10240", "NL49570", "HLL_221", "HLL_505", "NL10248", "NL49701", "HLL_450", "HLL_329", "HLL_284", "HLL_301", "NL49557", "NL01496", "HLL_223", "HLL_224", "NL53004", "NL01485", "HLL_458", "NL53001", "HLL_547", "HLL_440", "HLL_321", "HLL_256", "HLL_538", "HLL_470", "NL10444", "HLL_509", "HLL_293", "HLL_230", "HLL_474", "HLL_525", "NL49012", "HLL_453", "HLL_508", "HLL_235", "NL49553", "HLL_306", "NL10247", "HLL_315", "HLL_339", "HLL_533", "NL10641", "HLL_334", "NL10738", "HLL_332", "HLL_416", "HLL_341", "HLL_322", "HLL_350", "HLL_311", "HLL_330", "HLL_439", "HLL_278", "HLL_277", "NL49704", "HLL_418", "HLL_245", "NL01913", "HLL_537", "HLL_420", "HLL_526", "HLL_465", "HLL_383", "HLL_313", "NL10138", "HLL_433", "HLL_415", "HLL_237", "HLL_519", "HLL_328", "HLL_226", "HLL_469", "HLL_527", "HLL_429", "HLL_319", "HLL_391", "NL49572", "NL10136", "HLL_307", "NL10404", "HLL_463", "HLL_281", "HLL_297", "HLL_344", "NL49016", "NL10643", "HLL_419", "HLL_320", "NL10636", "NL10449", "HLL_325", "HLL_240", "NL10418", "HLL_448", "NL01488", "HLL_528", "HLL_343", "HLL_333", "NL10450", "NL01487", "HLL_473", "HLL_511", "NL49573", "HLL_545", "HLL_363", "NL10938", "NL10230", "NL49551", "NL10937", "NL01489", "HLL_430", "NL49561", "HLL_413"]
sensorListNL = ["NL10742", "NL49703", "NL01912", "NL01494", "NL10131", "NL49007", "NL01495", "NL01491", "NL10741", "NL10538", "NL49556", "NL10821", "NL10934", "NL10644", "NL49017", "NL10241", "NL49014", "NL10240", "NL49570", "NL10248", "NL49701", "NL49557", "NL01496", "NL53004", "NL01485", "NL53001", "NL10444", "NL49012", "NL49553", "NL10247", "NL10641", "NL10738", "NL49704", "NL01913", "NL10138", "NL49572", "NL10136", "NL10404", "NL49016", "NL10643", "NL10636", "NL10449", "NL10418", "NL01488", "NL10450", "NL01487", "NL49573", "NL10938", "NL10230", "NL49551", "NL10937", "NL01489", "NL49561"]
sensorListHLL = ["HLL_261", "HLL_288", "HLL_426", "HLL_549", "HLL_324", "HLL_259", "HLL_275", "HLL_475", "HLL_543", "HLL_298", "HLL_300", "HLL_462", "HLL_280", "HLL_410", "HLL_295", "HLL_424", "HLL_513", "HLL_441", "HLL_542", "HLL_323", "HLL_452", "HLL_506", "HLL_427", "HLL_345", "HLL_365", "HLL_512", "HLL_247", "HLL_532", "HLL_326", "HLL_541", "HLL_250", "HLL_531", "HLL_444", "HLL_291", "HLL_501", "HLL_476", "HLL_442", "HLL_438", "HLL_443", "HLL_434", "HLL_546", "HLL_221", "HLL_505", "HLL_450", "HLL_329", "HLL_284", "HLL_301", "HLL_223", "HLL_224", "HLL_458", "HLL_547", "HLL_440", "HLL_321", "HLL_256", "HLL_538", "HLL_470", "HLL_509", "HLL_293", "HLL_230", "HLL_474", "HLL_525", "HLL_453", "HLL_508", "HLL_235", "HLL_306", "HLL_315", "HLL_339", "HLL_533", "HLL_334", "HLL_332", "HLL_416", "HLL_341", "HLL_322", "HLL_350", "HLL_311", "HLL_330", "HLL_439", "HLL_278", "HLL_277", "HLL_418", "HLL_245", "HLL_537", "HLL_420", "HLL_526", "HLL_465", "HLL_383", "HLL_313", "HLL_433", "HLL_415", "HLL_237", "HLL_519", "HLL_328", "HLL_226", "HLL_469", "HLL_527", "HLL_429", "HLL_319", "HLL_391", "HLL_307", "HLL_463", "HLL_281", "HLL_297", "HLL_344", "HLL_419", "HLL_320", "HLL_325", "HLL_240", "HLL_448", "HLL_528", "HLL_343", "HLL_333", "HLL_473", "HLL_511", "HLL_545", "HLL_363", "HLL_430", "HLL_413"]

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
    snapshots = makeSnapshots(sensorListHLL, startdate, enddate, locations)

    maxpm25 = getMaxVal(sensorListHLL, "pm25")
    maxpm25 = 5 * (int((maxpm25 + 5) / 5))
    if maxpm25 > 150:
        maxpm25 = 150

    fig = px.scatter_mapbox(snapshots, lat='lat', lon='lon', color='pm25',
                            center=dict(lat=52.471, lon=4.810),
                            zoom=9,
                            # mapbox_style = 'open-street-map',
                            mapbox_style='carto-darkmatter',
                            range_color=(1, maxpm25),
                            opacity=0.9,
                            size="pm25",
                            size_max=20,
                            animation_frame="time",
                            animation_group="time"
    )

    fig.write_html("export.html")
    fig.show()

    printf("Done\n")
    return


# run stand alone entry point
if __name__ == '__main__':
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



