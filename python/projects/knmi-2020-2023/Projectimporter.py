import sys
sys.path.insert(0, '../..')
import importer as imp
import os

def runit():
    # should the datarange be included in the filename
    includedatesinfilename = False

    # location to save the datafiles. If None will save to default
    savelocation = os.getcwd()

    # startdate for retrieving
    start = "20200101"

    # enddate for retrieving (inclusive)
    end = "20230901"

    # not None if knmi-2020-2023 data must be retrieved
    knmiselection = ["240", "225", "209"] # schiphol, ijmuiden zuidpier, ijmuiden-zee
#    knmiselection = False

    # list of meetnet sensors to retrieve (include alfaprefix. None if nothing to retrieve
    meetnetselection = ["NL49556", "NL49016", "NL49012", "NL49014", "NL49007", "NL49017", "NL49570",
                        "NL49572", "NL49551", "NL49557", "NL49573", "NL49704", "NL49701", "NL49703"]

    meetnetselection = None

    # list sensors to retrieve. Every entry is a tuple: (project, sensornumber). None if nothing to retrieve
#    sensorselection = [("HLL", "549"), ("OZK", "1845"), ("HLL", "545"), ("OZK", "1850")]
    sensorselection = [("HLL", "298"),("HLL", "545"), ("HLL", "420")]
    sensorselection = None

    # fastimport: if True existing files will not be reloaded (no check on dates is done!)
    fastimport = True

    # when csv for sensordata not found, just continue (True), or end (False)
    ignorecsvnotfound = True

    imp.retrieveAllData(includedatesinfilename, savelocation, start, end, knmiselection, meetnetselection, sensorselection,
                        fastimport, ignorecsvnotfound)

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
