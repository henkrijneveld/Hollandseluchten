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
    start = "20231231"

    # enddate for retrieving (inclusive)
    end = "20240101"

    # not None if knmi data must be retrieved
    knmiselection = ["225"]
    knmiselection = False

    # list of meetnet sensors to retrieve
    meetnetselection = ["NL10418", "NL49570", "NL49701", "NL49556", "NL49561", "NL10641", "NL10636", "NL10538",
                        "NL10738", "NL10644", "NL10404", "NL49573", "NL49551", "NL49704",  "NL49017", "NL10641"
                        ]
    meetnetselection = ["NL01485", "NL01487", "NL01488", "NL01489", "NL01491", "NL01494", "NL01495", "NL01496",
                        "NL01912", "NL01913", "NL10131", "NL10136", "NL10138", "NL10230", "NL10240", "NL10241",
                        "NL10247", "NL10248", "NL10404", "NL10418", "NL10444", "NL10448", "NL10449", "NL10450",
                        "NL10538", "NL10636", "NL10641", "NL10643", "NL10644", "NL10738", "NL10741", "NL10742",
                        "NL10821", "NL10934", "NL10937", "NL10938", "NL49007", "NL49012", "NL49014", "NL49016",
                        "NL49017", "NL49551", "NL49553", "NL49556", "NL49557", "NL49561", "NL49570", "NL49572",
                        "NL49573", "NL49701", "NL49703", "NL49704", "NL53001", "NL53004"]
#    meetnetselection = None

    # list sensors to retrieve. Every entry is a tuple: (project, sensornumber). None if nothing to retrieve
#    sensorselection = None
    sensorselection = [("HLL", "298"), ("HLL", "462"), ("HLL", "532"),
                       ("HLL", "413"), ("HLL", "323"), ("HLL", "284"), ("HLL", "527"),
                       ("HLL", "350"), ("HLL", "546"), ("HLL", "250"), ("HLL", "509"),
                       ("HLL", "469"), ("HLL", "448"), ("HLL", "474"), ("HLL", "506"),
                       ("HLL", "439"), ("HLL", "334"), ("HLL", "415"), ("HLL", "458")]
    sensorselection = [("HLL", "221"),
    ("HLL", "223"),
    ("HLL", "224"),
    ("HLL", "226"),
    ("HLL", "230"),
    ("HLL", "235"),
    ("HLL", "237"),
    ("HLL", "240"),
    ("HLL", "245"),
    ("HLL", "247"),
    ("HLL", "250"),
    ("HLL", "256"),
    ("HLL", "259"),
    ("HLL", "261"),
    ("HLL", "275"),
    ("HLL", "277"),
    ("HLL", "278"),
    ("HLL", "280"),
    ("HLL", "281"),
    ("HLL", "284"),
    ("HLL", "288"),
    ("HLL", "291"),
    ("HLL", "293"),
    ("HLL", "295"),
    ("HLL", "297"),
    ("HLL", "298"),
    ("HLL", "300"),
    ("HLL", "301"),
    ("HLL", "306"),
    ("HLL", "307"),
    ("HLL", "311"),
    ("HLL", "313"),
    ("HLL", "315"),
    ("HLL", "319"),
    ("HLL", "320"),
    ("HLL", "321"),
    ("HLL", "322"),
    ("HLL", "323"),
    ("HLL", "324"),
    ("HLL", "325"),
    ("HLL", "326"),
    ("HLL", "328"),
    ("HLL", "329"),
    ("HLL", "330"),
    ("HLL", "332"),
    ("HLL", "333"),
    ("HLL", "334"),
    ("HLL", "339"),
    ("HLL", "341"),
    ("HLL", "343"),
    ("HLL", "344"),
    ("HLL", "345"),
    ("HLL", "350"),
    ("HLL", "363"),
    ("HLL", "365"),
    ("HLL", "383"),
    ("HLL", "391"),
    ("HLL", "410"),
    ("HLL", "413"),
    ("HLL", "415"),
    ("HLL", "416"),
    ("HLL", "418"),
    ("HLL", "419"),
    ("HLL", "420"),
    ("HLL", "424"),
    ("HLL", "426"),
    ("HLL", "427"),
    ("HLL", "429"),
    ("HLL", "430"),
    ("HLL", "433"),
    ("HLL", "434"),
    ("HLL", "438"),
    ("HLL", "439"),
    ("HLL", "440"),
    ("HLL", "441"),
    ("HLL", "442"),
    ("HLL", "443"),
    ("HLL", "444"),
    ("HLL", "448"),
    ("HLL", "450"),
    ("HLL", "452"),
    ("HLL", "453"),
    ("HLL", "458"),
    ("HLL", "462"),
    ("HLL", "463"),
    ("HLL", "465"),
    ("HLL", "469"),
    ("HLL", "470"),
    ("HLL", "473"),
    ("HLL", "474"),
    ("HLL", "475"),
    ("HLL", "476"),
    ("HLL", "501"),
    ("HLL", "505"),
    ("HLL", "506"),
    ("HLL", "508"),
    ("HLL", "509"),
    ("HLL", "511"),
    ("HLL", "512"),
    ("HLL", "513"),
    ("HLL", "519"),
    ("HLL", "525"),
    ("HLL", "526"),
    ("HLL", "527"),
    ("HLL", "528"),
    ("HLL", "531"),
    ("HLL", "532"),
    ("HLL", "533"),
    ("HLL", "537"),
    ("HLL", "538"),
    ("HLL", "541"),
    ("HLL", "542"),
    ("HLL", "543"),
    ("HLL", "545"),
    ("HLL", "546"),
    ("HLL", "547"),
    ("HLL", "549")]
    sensorselection = None

    # fastimport: if True existing files will not be reloaded (no check on dates is done!)
    fastimport = False

    # when csv for sensordata not found, just continue (True), or end (False)
    ignorecsvnotfound = True

    imp.retrieveAllData(includedatesinfilename, savelocation, start, end, knmiselection, meetnetselection, sensorselection,
                        fastimport, ignorecsvnotfound)

    return

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
