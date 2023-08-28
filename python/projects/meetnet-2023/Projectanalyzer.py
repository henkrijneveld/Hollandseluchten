# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

import sys
sys.path.insert(0, '../..')
from analyzer import *
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
startdate = "20230101"
enddate = "20230825"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/meetnet-2023"

def meanvalues(framelist):
    totalframe = pd.concat(framelist)
    totalframe.sort_values("datetime", inplace=True)
    result = totalframe.groupby("datetime")["pm25"].median().to_frame()
    result = result.reset_index()
    result.columns.values[0] = "datetime"
    result.columns.values[1] = "pm25"
    result["pm25_mean"] = totalframe.groupby("datetime")["pm25"].mean().values
    return result

# difplot on attribute name
def diffPlot(leftframe, rightframe, attr):
    merged = pd.merge(leftframe, rightframe, on='datetime', suffixes=("_left", "_right"))
    merged["delta_pm"] = merged.apply(lambda x: x[attr+"_left"] - x[attr+"_right"], axis=1)
    deltas = pd.DataFrame()
    deltas["delta_pm"] = merged["delta_pm"].copy()
    deltas.sort_values(inplace=True, ignore_index=True, by="delta_pm")
    print(deltas.describe())
    lplot = sns.histplot(data=deltas, x="delta_pm", binwidth=0.50, kde=True)
    lplot.set(xlim=(-20.0, 20.0))
    return

def runit():
    loc_beverwijk = meanvalues([NL49557, NL49573, NL49551, NL49572, NL49570])
    loc_midden = meanvalues([NL49556, NL49701, NL49704, NL49703])
    loc_amsterdam = meanvalues([NL49016, NL49012, NL49017, NL49014, NL49007])
    loc_all = meanvalues([NL49557, NL49573, NL49551, NL49572, NL49570, NL49556, NL49701,
                          NL49704, NL49703, NL49016, NL49012, NL49017, NL49014, NL49007])

    setGlobalPlot()
#    lplot = sns.lineplot(loc_all, x="datetime", y="pm25")
#    smootifyLineplot(lplot)

    diffPlot(loc_midden, loc_beverwijk, "pm25")
    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()
    plt.show()


