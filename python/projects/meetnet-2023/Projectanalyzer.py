# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

import sys

import matplotlib.pyplot as plt

sys.path.insert(0, '../..')
from analyzer import *
from plotter import *
import math
import pprint as pp

# GENERATED CONTENT:
# copy-paste output from function printGlobals() here
NL49704 = pd.DataFrame()
NL49551 = pd.DataFrame()
NL49557 = pd.DataFrame()
NL49701 = pd.DataFrame()
NL49573 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
NL49572 = pd.DataFrame()
NL49012 = pd.DataFrame()
NL49007 = pd.DataFrame()
NL49570 = pd.DataFrame()
NL49017 = pd.DataFrame()
NL49014 = pd.DataFrame()
NL49703 = pd.DataFrame()
NL49556 = pd.DataFrame()
NL49016 = pd.DataFrame()
HLL_298 = pd.DataFrame()
HLL_545 = pd.DataFrame()
HLL_420 = pd.DataFrame()

startdate = "20230101"
enddate = "20230825"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/meetnet-2023"


def runit():
    setGlobalPlot()

    loc_beverwijk = medianvalues([NL49557, NL49573, NL49551, NL49572, NL49570], "datetime", "pm25")
    loc_midden = medianvalues([NL49556, NL49701, NL49704, NL49703], "datetime", "pm25")
    loc_amsterdam = medianvalues([NL49016, NL49012, NL49017, NL49014, NL49007], "datetime", "pm25")
    loc_all = medianvalues([NL49557, NL49573, NL49551, NL49572, NL49570, NL49556, NL49701,
                          NL49704, NL49703, NL49016, NL49012, NL49017, NL49014, NL49007], "datetime", "pm25")


#    diff = diffFrame(HLL_545, HLL_298, "pm25")
#    diff = weatherFrame(HLL_420)
#    windplot(diff, "delta", True, True)

#    lplot = sns.lineplot(loc_all, x="datetime", y="pm25")
#    smootifyLineplot(lplot)

#    diffPlot(NL49573, NL49572, "pm25")

    hplot = sns.histplot(data=KNMI_240, x="winddirection",binwidth=10)
    hplot.set(xlim=(0, 370))
    plt.show()
    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



