# example url: https://api-samenmeten.rivm.nl/v1.0/Things?$filter=startswith(name,'HLL_hl_device_298')
# example url: https://api.luchtmeetnet.nl/open_api/stations/NL49701

import pandas as pd
import requests
import datetime
import os
import time

import sys
from sys import exit

def printf(format, *args):
    sys.stdout.write(format % args)

# Return in format:
# latitude (breedtegraad N-S), longitude (lengtegraad E-W)
def getLocationHLL(sensornumber):
    sensornumber = str(sensornumber)
    requestURL = ("https://api-samenmeten.rivm.nl/v1.0/Things?$filter=startswith(name,'HLL_hl_device_"+
                  sensornumber + "')")
    sensordata = requests.get(requestURL)
    if sensordata.status_code != 200:
        printf("Error reading sensordata %s. Status code = %d\n", sensornumber, sensordata.status_code)
        exit(-1)
    sensordict = sensordata.json()['value']
    locationLink = sensordict[0]['Locations@iot.navigationLink']

    locations = requests.get(locationLink)
    if locations.status_code != 200:
        printf("Error reading locations for sensordata %s. Status code = %d\n", sensornumber, locations.status_code)
        exit(-1)
    locationdict = locations.json()['value'][0]
    locationlist = locationdict['location']['coordinates']
    if len(locationlist) != 2:
        printf("Locationlist for sensor %s different from 2\n", sensornumber)
        printf("API Link: %s\n", locationLink)
        exit(-1)

    return(locationlist[1], locationlist[0])

def getLocationMeetnet(sensornumber):
    sensornumber = str(sensornumber)
    if not sensornumber.startswith("NL"):
        sensornumber = "NL" + sensornumber
    requestURL = ("https://api.luchtmeetnet.nl/open_api/stations/" + sensornumber)
    sensordata = requests.get(requestURL)
    if sensordata.status_code != 200:
        printf("Error reading sensordata %s. Status code = %d\n", sensornumber, sensordata.status_code)
        exit(-1)
    sensordict = sensordata.json()['data']
    locationlist = sensordict['geometry']['coordinates']
    if len(locationlist) != 2:
        printf("Locationlist for sensor %s different from 2\n", sensornumber)
        printf("API Link: %s\n", requestURL)
        exit(-1)

    return(locationlist[1], locationlist[0])

# Retrieves location for a list of sensors
# sensorname can be:
# a tuple: project and number (project is HLL or OVK)
# a string: identification of a meetnet sensor
#
# if locationList exists positions will only be retrieved if the sensor is not in it
#
# return: a dataframe with sensor (HLL_number, OVK_number, NLnumber)
# lat (latitude) and lon (longitude)
def getLocations(sensorList, locationList = None):
    if locationList is None:
        locationList = pd.DataFrame(columns=["sensor", "lat", "lon"])
        locationList = locationList.astype({'sensor': 'string', 'lat': 'float', 'lon': 'float'})

    sensorposition = None
    for sensor in sensorList:
        sensorname = None
        if isinstance(sensor, str):
            sensorname = sensor
            sensorposition = getLocationMeetnet(sensorname)
        if isinstance(sensor, tuple):
            if sensor[0] == "HLL":
                sensorname = "HLL_" + sensor[1]
                sensorposition = getLocationHLL(sensor[1])
        if sensorname is None:
            printf("Unsupported sensorname %s - %s\n", sensor[0], sensor[1])
            exit(-1)
        locationList.loc[len(locationList)] = [sensorname, sensorposition[0], sensorposition[1]]

    return locationList


def runit():
    loc298 = getLocationHLL(298)
    printf("298 is on lat %f, lon %f\n", loc298[0], loc298[1])
    loc49570 = getLocationMeetnet("NL49570")
    printf("NL49570 is on lat %f, lon %f\n", loc49570[0], loc49570[1])

    loclist = getLocations([("HLL", "298")])
    loclist = getLocations(["NL49570"], loclist)

    return

if __name__ == '__main__':
    runit()

