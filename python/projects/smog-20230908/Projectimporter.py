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
    start = "20230908"

    # enddate for retrieving (inclusive)
    end = "20230909"

    # not None if knmi data must be retrieved
    knmiselection = ["225"]
    knmiselection = False

    # list of meetnet sensors to retrieve
    meetnetselection = ["NL10418", "NL49570", "NL49701", "NL49556", "NL49561", "NL10641", "NL10636", "NL10538",
                        "NL10738", "NL10644", "NL10404", "NL49573", "NL49551", "NL49704",  "NL49017", "NL10641"
                        ]

#    meetnetselection = None

    # list sensors to retrieve. Every entry is a tuple: (project, sensornumber). None if nothing to retrieve
#    sensorselection = None
    sensorselection = [("HLL", "298"), ("HLL", "462"), ("HLL", "532"),
                       ("HLL", "413"), ("HLL", "323"), ("HLL", "284"), ("HLL", "527"),
                       ("HLL", "350"), ("HLL", "546"), ("HLL", "250"), ("HLL", "509"),
                       ("HLL", "469"), ("HLL", "448"), ("HLL", "474"), ("HLL", "506"),
                       ("HLL", "439"), ("HLL", "334"), ("HLL", "415"), ("HLL", "458")]


    # fastimport: if True existing files will not be reloaded (no check on dates is done!)
    fastimport = False

    # when csv for sensordata not found, just continue (True), or end (False)
    ignorecsvnotfound = False

    imp.retrieveAllData(includedatesinfilename, savelocation, start, end, knmiselection, meetnetselection, sensorselection,
                        fastimport, ignorecsvnotfound)

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
