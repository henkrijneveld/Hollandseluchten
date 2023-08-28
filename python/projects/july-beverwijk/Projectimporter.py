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
    start = "20230601"

    # enddate for retrieving (inclusive)
    end = "20230731"

    # not None if knmi data must be retrieved
    knmiselection = True
#    knmiselection = False

    # list of meetnet sensors to retrieve (include alfaprefix. None if nothing to retrieve
#    meetnetselection = ["NL49570", "NL49572", "NL49551", "NL49557", "NL49573", "NL49704", "NL49701", "NL49703"]
    meetnetselection = ["NL49570"]
#    meetnetselection = None

    # list sensors to retrieve. Every entry is a tuple: (project, sensornumber). None if nothing to retrieve
    sensorselection = [("HLL", "549"), ("OZK", "1845"), ("HLL", "545"), ("OZK", "1850")]
#    sensorselection = None

    fastimport=True

    imp.retrieveAllData(includedatesinfilename, savelocation, start, end, knmiselection, meetnetselection, sensorselection, fastimport)

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
