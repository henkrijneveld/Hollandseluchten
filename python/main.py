# Prerequisites:
# - panda and dependencies installed
# ../data-raw: tafik csv files
# ../data_knmi: destination knmi files
# ../data-sensors: destination project sensor files
# ../data-meetnet: destination meetnet files
#
# API INFO
# samen meten (alleen de sensors van de citizens)
# https://api-samenmeten.rivm.nl/v1.0/Things?$filter=startswith(name,%27HLL_hl_device_298%27)
# zou dus allemaal in de Tafik bestanden moeten staan
# tijd is UTC (Zulu tijd)
#
# RIVM
# https://api.luchtmeetnet.nl/open_api/stations/NL49701
# waardes van een dag voor de Zaanse sensor
# https://api.luchtmeetnet.nl/open_api/measurements?station_number=NL49701&formula=PM25&page=1&order_by=timestamp_measured&order_direction=desc&end=2023-08-13T23:59:00&start=2023-08-13T00:00:00
# tijd is UTC (Zulu tijd)
#
# KNMI
# https://www.daggegevens.knmi.nl/klimatologie/uurgegevens?start=2023081301&end=2023081324&fmt=json&stns=240
# Alle stationnummers en veldnamen gespecificeerd: https://daggegevens.knmi.nl/
# tijd is UTC (Zulu tijd). Startuur 1 in de aanroep levert 00:00Z op.

import pandas as pd
import matplotlib.pyplot as plt
import requests
import datetime

import sys
def printf(format, *args):
    sys.stdout.write(format % args)


# get KNMI data
# station: numerical string ("240" is Schiphol)
# start: startdate string, format YYYYMMDD
# end: enddate string, format YYYYMMDD
#
# return: Dataframe. Columns:
#  timestamp (date and hour in original data)
#  winddirection (DD in original data)
#  windspeed (FF / 10 in original data)
#  temperature (T in original data)
#  humidity (U in original data)
#
# WARNING: do not call this function too often, you will be blocked!
# do to the specific way knmi api works, allways start a day earlier with retrieving the data
def dateadd(x):
    x["datetime"] = x["datetime"] + pd.Timedelta(hours = x["hour"])
    return x

def getKNMI(station, start, end):
    requestURL = ("https://www.daggegevens.knmi.nl/klimatologie/uurgegevens?start="+start+"01&end="+end+
                  "24&fmt=json&stns="+station+"&vars=DD:FF:T:U")
    knmidata = requests.get(requestURL)
    #requestPOSTURL = "https://www.daggegevens.knmi.nl/klimatologie/uurgegevens"
    #postdata = {'start': start+'01', 'end': end+"24", 'fmt': 'json', 'stns': station, 'vars': 'DD:FF:T:U'}
    #knmidata = requests.post(requestPOSTURL, json = postdata)

    if knmidata.status_code != 200:
        printf("Error reading knmi station %s. Status code = %d", station, knmidata.status_code)
        exit(-1)
    knmidict = knmidata.json()
    if len(knmidict) == 0:
        printf("No data received from KNMI\n")
        exit(-1)
    knmiframe = pd.DataFrame.from_dict(knmidict)
    knmiframe.rename(columns={'date': 'datetime', 'DD': 'winddirection',
                                'FF': 'windspeed', 'T': 'temperature', 'U': 'humidity'}, inplace=True)
    knmiframe["datetime"] = pd.to_datetime(knmiframe["datetime"])
    # add hour to datetime, as all the values are from the last part of the hour
    knmiframe = knmiframe.apply(dateadd, axis = 1)
    knmiframe = knmiframe.astype({'winddirection' : 'int'})
    knmiframe = knmiframe.astype({'humidity' : 'int'})
    knmiframe = knmiframe.astype({'windspeed' : 'float64'})
    knmiframe['windspeed'] = knmiframe['windspeed'].apply(lambda x: x / 10)
    knmiframe = knmiframe.astype({'temperature' : 'float64'})
    knmiframe['temperature'] = knmiframe['temperature'].apply(lambda x: x / 10)
    knmiframe.drop(columns=['station_code','hour'], inplace=True)
    printf("KNMI data retrieved!\n")
    return knmiframe

# convert YYYYMMDD to YYY-MM-DD
def convertToHyphenatedDate(aDate):
    return (aDate[0:4] + "-" + aDate[4:6] + "-" + aDate[6:8])

def getMeetnetTimelimited(sensor, start, end):
    start = convertToHyphenatedDate(start)
    end = convertToHyphenatedDate(end)
    requestURL = ("https://api.luchtmeetnet.nl/open_api/measurements?station_number="+sensor+"&formula=PM25&page=1&order_by=timestamp_measured&order_direction=desc&end="+
                  end+"T23:59:00&start="+start+"T00:00:00")
    luchtmeetdata = requests.get(requestURL)
    if luchtmeetdata.status_code != 200:
        printf("Error reading luchtmeetdata %s. Status code = %d", sensor, luchtmeetdata.status_code)
        exit(-1)
    luchtmeetdict = luchtmeetdata.json()['data']
    luchtdata = pd.DataFrame.from_dict(luchtmeetdict)
    luchtdata.rename(columns={'value': 'pm25', 'timestamp_measured': 'datetime'}, inplace=True)

    luchtdata = luchtdata.astype({'pm25' : 'float64'})
    luchtdata["datetime"] = pd.to_datetime(luchtdata["datetime"])
    luchtdata.drop(columns=['station_number','formula'], inplace=True)
    luchtdata.sort_values(by=['datetime'], inplace=True)
    printf("Luchtmeet data retrieved from %s to %s!\n", start, end)
    return luchtdata

def convertToDatetime(aDate):
    return datetime.date(int(aDate[0:4]), int(aDate[4:6]), int(aDate[6:8]))

def getMeetnet(sensor, start, end):
    # the noobs at meetnet only allow 7 days at once ;/
    dt_start = convertToDatetime(start)
    dt_tmpend = convertToDatetime(start) + datetime.timedelta(days=6)
    dt_end = convertToDatetime(end)
    if dt_tmpend > dt_end:
        dt_tmpend = dt_end
    meetframe = getMeetnetTimelimited(sensor, dt_start.strftime("%Y%m%d"), dt_tmpend.strftime("%Y%m%d"))
    #    printf("start %s to end %s\n", dt_start.strftime("%Y%m%d"), dt_tmpend.strftime("%Y%m%d"))

    while dt_tmpend < dt_end:
        dt_start = dt_tmpend + datetime.timedelta(days=1)
        dt_tmpend = dt_start + datetime.timedelta(days=6)
        if dt_tmpend > dt_end:
            dt_tmpend = dt_end
        meetframe = pd.concat(
            [meetframe, getMeetnetTimelimited(sensor, dt_start.strftime("%Y%m%d"), dt_tmpend.strftime("%Y%m%d"))],
            ignore_index=True)
#        printf("start %s to end %s\n", dt_start.strftime("%Y%m%d"), dt_tmpend.strftime("%Y%m%d"))-
    return meetframe

# key for sensor values is the name + postfix
def getCSVsensordate(name, date, postfix_pm25, postfix_temp, postfix_rh, postfix_pres):
    csvfile = "../data-raw/kogerveldData_" + date +".csv"
    all = pd.read_csv(csvfile)
    pm25frame = all.query("name=='" + name + postfix_pm25 + "'").copy()
    pm25frame.rename(columns={'result': 'pm25', 'phenomenonTime': 'datetime'}, inplace=True)
    pm25frame.drop(columns=['@iot.id','name', 'unitOfMeasurement.symbol'], inplace=True)

    tempframe = all.query("name=='" + name + postfix_temp + "'").copy()
    tempframe.rename(columns={'result': 'temperature', 'phenomenonTime': 'datetime'}, inplace=True)
    tempframe.drop(columns=['@iot.id','name', 'unitOfMeasurement.symbol'], inplace=True)

    rhframe = all.query("name=='" + name + postfix_rh + "'").copy()
    rhframe.rename(columns={'result': 'humidity', 'phenomenonTime': 'datetime'}, inplace=True)
    rhframe.drop(columns=['@iot.id','name', 'unitOfMeasurement.symbol'], inplace=True)

    meetframe = pm25frame.merge(tempframe, how='outer', on='datetime')
    meetframe = meetframe.merge(rhframe, how='outer', on='datetime')

    meetframe = meetframe.astype({'pm25' : 'float64'})
    meetframe = meetframe.astype({'temperature' : 'float64'})
    meetframe = meetframe.astype({'humidity' : 'float64'})
    meetframe["datetime"] = pd.to_datetime(meetframe["datetime"])

    meetframe.sort_values(by=['datetime'], inplace=True)
    printf(".")
    return meetframe

def getCSVsensor(project, sensor, start, end):
    sensorname = None
    postfix_pm25 = None
    postfix_temp = None
    postfix_rh = None
    postfix_pres = None

    if project == "OZK":
        sensorname = "OZK" + sensor
        postfix_pres = "-4-pres"
        postfix_rh = "-4-rh"
        postfix_temp = "-4-temp"
        postfix_pm25 = "-12-pm25"

    if project == "HLL":
        sensorname = "HLL_hl_device_" + sensor
        postfix_pm25 = "-12-pm25"
        postfix_temp = "-6-temp"
        postfix_rh = "-6-rh"

    if sensorname == None:
      printf("Sensor not specified or project unknown!\n")
      exit(-1)

    printf("Progress for %s: ", sensorname)

    dt_start = convertToDatetime(start)
    dt_tmpend = convertToDatetime(start) + datetime.timedelta(days = 1)
    dt_end = convertToDatetime(end)

    meetframe = getCSVsensordate(sensorname, dt_start.strftime("%Y%m%d"), postfix_pm25, postfix_temp, postfix_rh, postfix_pres)

    while dt_tmpend <= dt_end:
        dt_start = dt_tmpend
        dt_tmpend = dt_start + datetime.timedelta(days=1)
        meetframe = pd.concat(
            [meetframe, getCSVsensordate(sensorname, dt_start.strftime("%Y%m%d"), postfix_pm25, postfix_temp, postfix_rh, postfix_pres)],
            ignore_index=True)

    return meetframe



def runKNMItofile():
    start = "20230101"
    end = "20230816"
    station = "420"
    knmidata = getKNMI(station, start, end)
    savefile = "../data-knmi/" + station + "-" + start + "-" + end + ".csv"
    knmidata.to_csv(savefile)

def runMeetnettofile():
    start = "20230101"
    end = "20230816"
    sensor = "NL49701"
    meetframe = getMeetnet(sensor, start, end)
    savefile = "../data-meetnet/" + sensor + "-pm25-" + start + "-" + end + ".csv"
    meetframe.to_csv(savefile)

def runCSVtofile():
    start = "20230701"
    end = "20230810"
    project = "HLL"
    sensor = "298"
    meetframe = getCSVsensor(project, sensor, start, end)
    savefile = "../data-sensors/" + project + "-" + sensor + "-" + start + "-" + end + ".csv"
    meetframe.to_csv(savefile)

def runit():
    runKNMItofile()
#    runMeetnettofile()
#    runCSVtofile()
    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
