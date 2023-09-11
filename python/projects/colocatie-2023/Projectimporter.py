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
    start = "20230101"

    # enddate for retrieving (inclusive)
    end = "20230901"

    # not None if knmi data must be retrieved
    knmiselection = ["240", "225"]
#    knmiselection = False

    # list of meetnet sensors to retrieve
    meetnetselection = ["NL49570", "NL49701"]

#    meetnetselection = None

    # list sensors to retrieve. Every entry is a tuple: (project, sensornumber). None if nothing to retrieve
#    sensorselection = [("HLL", "549"), ("OZK", "1845"), ("HLL", "545"), ("OZK", "1850")]
    sensorselection = None
    sensorselection = [("HLL", "420"),("HLL", "541"), ("OZK", "1849"), ("HLL", "549"), ("HLL", "545"), ("OZK", "1850"),
                       ("OZK", "1845"), ("HLL", "298"), ("HLL", "433"), ("HLL", "452"), ("HLL", "226"), ("HLL", "513")]

    # fastimport: if True existing files will not be reloaded (no check on dates is done!)
    fastimport = True

    # when csv for sensordata not found, just continue (True), or end (False)
    ignorecsvnotfound = False

    imp.retrieveAllData(includedatesinfilename, savelocation, start, end, knmiselection, meetnetselection, sensorselection,
                        fastimport, ignorecsvnotfound)

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
