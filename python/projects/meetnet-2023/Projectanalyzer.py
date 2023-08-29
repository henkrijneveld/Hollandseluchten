# Prerequisites:
# - panda and dependencies installed
# - csv projects in directory

import sys
sys.path.insert(0, '../..')
from analyzer import *
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

# the framelist values are concatenated, and the median and mean values are determined on the groupby attribute
# a dataframe with a single row for every groupby value is returned
def medianvalues(framelist, groupby, value):
    totalframe = pd.concat(framelist)
    totalframe.sort_values(groupby, inplace=True)
    result = totalframe.groupby(groupby)[value].median().to_frame()
    result = result.reset_index()
    result.columns.values[0] = groupby
    result.columns.values[1] = value
    result[value+"_mean"] = totalframe.groupby(groupby)[value].mean().values
    return result

def diffFrame(leftframe, rightframe, attr):
    merged = pd.merge(leftframe, rightframe, on='datetime', suffixes=("_left", "_right"))
    merged["delta"] = merged.apply(lambda x: x[attr+"_left"] - x[attr+"_right"], axis=1)
    deltas = pd.DataFrame()
    deltas["delta"] = merged["delta"].copy()
    deltas["datetime"] = merged["datetime"].copy()
    deltas.sort_values(inplace=True, ignore_index=True, by="delta")
    print(deltas.describe())
    return deltas

# difplot on attribute name
def diffPlot(leftframe, rightframe, attr):
    deltas = diffFrame(leftframe, rightframe, attr)
    lplot = sns.histplot(data=deltas, x="delta", binwidth=0.50, kde=True)
    lplot.set(xlim=(-40.0, 20.0))
    return

def windplot(frame, values, polar=True, useMedian=True):
    conc = weatherFrame(frame)
    conc = medianvalues([conc], "winddirection", values)
    if not useMedian:
        values = values + "_mean"
    if polar:
        conc["winddirection"] = conc["winddirection"] / 180 * math.pi
        conc.drop(index=37, inplace=True) # this is value 990: variable winds
        conc.loc[0] = conc.loc[36].copy() # direction 0: no wind
        conc["winddirection"][0] = 0
        g = sns.FacetGrid(conc, subplot_kws=dict(projection='polar', theta_offset=math.pi/2, theta_direction=-1), height=10,
                          sharex=False, sharey=False, despine=False)
        g.map_dataframe(sns.lineplot, x="winddirection", y=values, linewidth=4.0)
    else:
        lplot = (sns.scatterplot(data=conc, x="winddirection", y=values))
        lplot.set(xlim=(5.0, 365.0))

# merge knmi data into a frame
def weatherFrame(aFrame):
    conc = pd.merge(aFrame, KNMI_240, on="datetime", suffixes=("", "_knmi"))
    conc = conc.rename({'windspeed_knmi': 'windspeed', 'winddirection_knmi': 'winddirection'}, axis=1)
    return conc

def runit():
    setGlobalPlot()

    loc_beverwijk = medianvalues([NL49557, NL49573, NL49551, NL49572, NL49570], "datetime", "pm25")
    loc_midden = medianvalues([NL49556, NL49701, NL49704, NL49703], "datetime", "pm25")
    loc_amsterdam = medianvalues([NL49016, NL49012, NL49017, NL49014, NL49007], "datetime", "pm25")
    loc_all = medianvalues([NL49557, NL49573, NL49551, NL49572, NL49570, NL49556, NL49701,
                          NL49704, NL49703, NL49016, NL49012, NL49017, NL49014, NL49007], "datetime", "pm25")


    diff = diffFrame(HLL_545, HLL_298, "pm25")
#    diff = weatherFrame(HLL_420)
    windplot(diff, "delta", True, True)

#    lplot = sns.lineplot(loc_all, x="datetime", y="pm25")
#    smootifyLineplot(lplot)

#    diffPlot(NL49573, NL49572, "pm25")
    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()
    plt.show()


