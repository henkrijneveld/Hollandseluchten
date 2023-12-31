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

NL49704 = pd.DataFrame()
NL49551 = pd.DataFrame()
KNMI_225 = pd.DataFrame()
NL49557 = pd.DataFrame()
NL49701 = pd.DataFrame()
NL49573 = pd.DataFrame()
NL49561 = pd.DataFrame()
HLL_298 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
NL49553 = pd.DataFrame()
NL49572 = pd.DataFrame()
HLL_545 = pd.DataFrame()
NL49012 = pd.DataFrame()
NL49007 = pd.DataFrame()
HLL_420 = pd.DataFrame()
KNMI_209 = pd.DataFrame()
NL49570 = pd.DataFrame()
NL49017 = pd.DataFrame()
NL49014 = pd.DataFrame()
NL49703 = pd.DataFrame()
NL49556 = pd.DataFrame()
NL49016 = pd.DataFrame()
startdate = "20230101"
enddate = "20230901"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/meetnet-2023"


def runit():
    # list of meetnet sensors to retrieve
    selectionwest = [NL49553, NL49557, NL49573, NL49570, NL49572, NL49551]
    selectionmiddle = [NL49561, NL49703, NL49704, NL49701, NL49556]
    selectioneast = [NL49007, NL49016, NL49012, NL49014, NL49017]
    selectionall = selectionwest + selectionmiddle + selectioneast


    setGlobalPlot()

    westdata = pd.concat(selectionwest)
    middledata = pd.concat(selectionmiddle)
    eastdata = pd.concat(selectioneast)

    loc_west = medianvalues([westdata], "datetime", "pm25")
    loc_middle = medianvalues([middledata], "datetime", "pm25")
    loc_east = medianvalues([eastdata], "datetime", "pm25")
    loc_all = medianvalues([westdata, middledata, eastdata], "datetime", "pm25")
#    loc_all = meanvalues([westdata, middledata, eastdata], "datetime", "pm25")


    # create the virtual reference sensor
    loc_all = removeDatesBefore(loc_all, "2023-01-01 04:00:00+00:00")  # remove the fireworks peak at 1th januari
    loc_all.to_csv("NLMedian.csv")

    # plot the median pm concentrations of the virtual sensor
    lplot = sns.lineplot(loc_all, x="datetime", y="pm25")
    lplot.set(title="NLMedian sensor (all NL sensors, median value")
    smootifyLineplot(lplot)
    plt.show()
    lplot.get_figure().savefig(projectdir + "/NLMediansensor")

    plotPM25series(loc_all, title="PM25 concentration all stations vs winddirection Schiphol",
                   knmiFrame=KNMI_240, method="meanvalues", filename=projectdir+"/PM25-median-wind-schiphol")


    # colocationsensors
    #  49570: Beverwijk
    #  49701: Zaandam

    # winddependency
    plotPM25series(NL49570, title="PM25 concentration coloc NL49570 vs winddirection IJmuiden Zuidpier", knmiFrame=KNMI_225, filename=projectdir+"/PM25-coloc-NL49570")
    plotPM25series(NL49701, title="PM25 concentration coloc NL49701 vs winddirection Schiphol", knmiFrame=KNMI_240, filename=projectdir+"/PM25-coloc-NL49701")
    plotPM25series(NL49561, title="PM25 concentration NL49561 (closest to Schiphol) vs winddirection Schiphol", knmiFrame=KNMI_240, filename=projectdir+"/PM25-Schiphol-NL49561")

    # difference from reference
    diffPlot(NL49556, loc_all, attr="pm25", title="difference NL49556 (de Rijp) vs reference", filename=projectdir+"/PM25-deRijp-diff")
    diffPlot(NL49570, loc_all, attr="pm25", title="difference NL49570 vs reference", filename=projectdir+"/PM25-NL49570-diff")
    diffPlot(NL49701, loc_all, attr="pm25", title="difference NL49701 vs reference", filename=projectdir+"/PM25-NL49701-diff")
    diffPlotRelative(NL49701, loc_all, xlim=(-0.5, 4.0), attr="pm25", title="Relative difference coloc zaandam 49701 vs reference", filename=projectdir+"/PM25-NL49701--Relative-diff")

    # situational plots
    # industry Beverwijk
    #  49573: west sensor
    #  49572: east sensor
    #  49557: north sensor
    #  49551: south sensor
    plotDiff25(NL49573, NL49572, title="Difference West - East industry Beverwijk", knmiFrame=KNMI_225, filename=projectdir+"/PM25-WE-Beverwijk")
    plotDiff25(NL49557, NL49551, title="Difference North - South industry Beverwijk", knmiFrame=KNMI_225, filename=projectdir+"/PM25-NS-Beverwijk")
    diffPlot(NL49557, loc_all, xlim=(-15.0, 15.0), attr="pm25", title="difference NL49557 (North industry Beverwijk) vs reference", filename=projectdir+"/PM25-N-Beverwijk-diff-ref")
    diffPlotRelative(NL49557, loc_all, xlim=(-0.5, 4.0), attr="pm25", title="Relative difference NL49557 (North industry Beverwijk) vs reference", filename=projectdir+"/PM25-N-Beverwijk-reldiff-ref")
    diffPlot(NL49551, loc_all, xlim=(-15.0, 15.0), attr="pm25", title="difference NL49551 (South industry Beverwijk) vs reference", filename=projectdir+"/PM25-S-Beverwijk-diff-ref")

    # Amsterdam including highways
    # 49561: schiphol
    # 49017: Amsterdam east
    plotDiff25(NL49561, NL49017, title="Difference Schiphol NL49561 - Amsterdam NL49017", knmiFrame=KNMI_240, filename=projectdir+"/PM25-Schiphol-Amsterdam-East")

    # remote distance from beverwijk
    #  49556: de rijp
    #  49701: zaanstad
    #  49703: halfweg
    plotDiff25(NL49556, NL49703, title="Difference North (NL49556 de Rijp) and south (NL49703 Halfweg)", knmiFrame=KNMI_240, filename=projectdir+"/diff-PM25-deRijp-Halfweg")
    plotDiff25(NL49556, NL49561, title="Difference North (NL49556 de Rijp) and south (NL49561 Schiphol)", knmiFrame=KNMI_240, filename=projectdir+"/diff-PM25-deRijp-Schiphol")
    plotDiff25(NL49556, NL49704, title="Difference North (NL49556 de Rijp) and south (NL49704 Zaanstadd)", knmiFrame=KNMI_240, filename=projectdir+"/diff-PM25-deRijp-Zaanstad")
    plotDiff25(NL49704, NL49561, title="Difference North (NL49704 Zaanstad) and south (NL49704 Schiphol)", knmiFrame=KNMI_240, filename=projectdir+"/diff-PM25-Zaanstad-Schiphol")

    return

    # plot the max pm concentrations of all the sensors
    loc_all_max = maxvalues([westdata, middledata, eastdata], "datetime", "pm25")
    lplot = sns.lineplot(loc_all_max, x="datetime", y="pm25")
    smootifyLineplot(lplot)
    plt.show()
    plt.savefig(projectdir + "/NLMediansensor")

    # plot the min concentrations of all the sensors
    loc_all_min = minvalues([westdata, middledata, eastdata], "datetime", "pm25")
    lplot = sns.lineplot(loc_all_min, x="datetime", y="pm25")
    smootifyLineplot(lplot)
    plt.show()

    # plot the number of negative values in a histogram
    loc_all_negative = pd.concat(selectionall)
    loc_all_negative = loc_all_negative[loc_all_negative["pm25"] < 0].copy()
    windPM_all_negative = weatherFrame(loc_all_negative, KNMI_240)
    windcountplot(windPM_all_negative, title="number of counts with negative values")
    windPM_all = weatherFrame(loc_all, KNMI_240)
    windcountplot(windPM_all, title="number of counts with all values")
    q = windPM_all_negative.nunique(dropna="sensorname")

    # Median values of pm25
    plotPM25series(loc_all, title="PM25 concentration all stations vs winddirection Schiphol", knmiFrame=KNMI_240)
    plotPM25series(loc_west, title="West PM25 data 2023 vs winddirection Schiphol", knmiFrame=KNMI_240)
    plotPM25series(loc_middle, title="Middle PM25 data 2023 vs winddirection Schiphol", knmiFrame=KNMI_240)
    plotPM25series(loc_east, title="East PM25 data 2023vs winddirection Schiphol", knmiFrame=KNMI_240)
    plotPM25series(loc_west, title="West PM25 data 2023 vs winddirection IJmuiden Zuidpier", knmiFrame=KNMI_225)

    # setup wind concentrationplots on the mediam
#    plotPM25series(loc_all, "PM25 concentration all stations vs winddirection Schiphol", KNMI_240)
#    plotPM25series(loc_west, "West PM25 data 2023", KNMI_240)
#    plotPM25series(loc_middle, "Middle PM25 data 2023", KNMI_240)
#    plotPM25series(loc_east, "East PM25 data 2023", KNMI_240)
    plotPM25series(loc_all, "All PM25 data 2023 - median", KNMI_240)
    plotPM25series(loc_all_mean, "All PM25 data 2023 - mean", KNMI_240, "meanvalues")
    plotPM25series(loc_all_max, "All PM25 data 2023 - max", KNMI_240, "maxvalues")
    plotPM25series(loc_all_min, "All PM25 data 2023 - min", KNMI_240, "minvalues")

#    plotPM25series(NL49561, "Meetnetsensor 49561 (Schiphol next to knmi station)", KNMI_240)

#    plotPM25series(NL49573, "Meetnetsensor 49573 (West Beverwijk)", KNMI_225)
#    plotPM25series(NL49551, "Meetnetsensor 49551 (South Beverwijk)", KNMI_225)
#    plotPM25series(NL49572, "Meetnetsensor 49572 (East Beverwijk)", KNMI_225)
#    plotPM25series(NL49557, "Meetnetsensor 49557 (North Beverwijk)", KNMI_225)

#    plotDiff25(NL49573, NL49572, "East-West meetnet Beverwijk", KNMI_225)
#    plotDiff25(NL49551, NL49557, "North-South meetnet Beverwijk", KNMI_225)
#    plotDiff25(NL49016, NL49012, "West - East detectors Beverwijk", KNMI_240)
#    plotDiff25(NL49553, NL49557, "Top North detectors Beverwijk", KNMI_240)



#    diff = diffFrame(HLL_545, HLL_298, "pm25")
#    diff = weatherFrame(HLL_420)
#    windplot(diff, "delta", True, True)

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



