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
    end = "20231001"

    # not None if knmi data must be retrieved
    knmiselection = ["240"]
#    knmiselection = False

    # list of meetnet sensors to retrieve
    meetnetselection = ["NL49701", "NL49556"]   # colocatie NL Zaandam
#    meetnetselection = None

    # list sensors to retrieve. Every entry is a tuple: (project, sensornumber). None if nothing to retrieve
#    sensorselection = None
    sensorselection = [("HLL", "298"), ("HLL", "320"), ("HLL", "256"), ("HLL", "326"), ("HLL", "339"), ("HLL", "325"),
                       ("HLL", "345"), ("HLL", "307"), ("HLL", "448"), ("HLL", "531"), ("HLL", "378"), ("HLL", "415")]

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
