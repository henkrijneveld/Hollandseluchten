# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

import sys
sys.path.insert(0, '../..')
from analyzer import *
import pprint as pp

# GENERATED CONTENT:
# copy-paste output from function printGlobals() here
NL49703 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
NL49570 = pd.DataFrame()
NL49701 = pd.DataFrame()
NL49557 = pd.DataFrame()
NL49704 = pd.DataFrame()
NL49572 = pd.DataFrame()
NL49573 = pd.DataFrame()
NL49551 = pd.DataFrame()
startdate = "20230601"
enddate = "20230731"
projectdir = "/home/henk/Projects/Hollandse-Luchten/python/projects/meetnet-2023"

def runit():
    setGlobalPlot()
    merged = pd.merge(NL49701, NL49704, on='datetime', suffixes=("_first", "_last"))
    merged["delta_pm"] = merged.apply(lambda x: x["pm25_first"] - x["pm25_last"], axis=1)#
    deltas = pd.DataFrame()
    deltas["delta_pm"] = merged["delta_pm"].copy()
    deltas.sort_values(inplace=True, ignore_index=True, by="delta_pm")
    lplot = sns.histplot(data=deltas, x="delta_pm", binwidth=0.20, kde=True)
    lplot.set(xlim=(-50.0, 50.0))
    return

# run stand alone entry point
if __name__ == '__main__':
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()
    plt.show()


