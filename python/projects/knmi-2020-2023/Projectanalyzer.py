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

KNMI_225 = pd.DataFrame()
KNMI_240 = pd.DataFrame()
KNMI_209 = pd.DataFrame()
startdate = "20200101"
enddate = "20230901"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/knmi-2020-2023"

def runit():
    setGlobalPlot()

    diffWindPlot(KNMI_209, KNMI_225, title="Difference direction KNMI_209 vs KNMI_225 (2020-2023)")
    diffWindPlot(KNMI_240, KNMI_225, title="Difference direction KNMI_240 vs KNMI_225 (2020-2023)")


#   WINDDIRECTION COUNTS FOR STATION AND YEAR
#    windcountplot(KNMI_240, True, "Windcountplot Schiphol (240) from "+startdate+" to "+enddate)
#    KNMI_240_2023 = KNMI_240[KNMI_240["datetime"] < pd.to_datetime("2021-01-01 21:00:00+00:00")].copy()
#    windcountplot(KNMI_240_2023, True, "Windcountplot Schiphol (240) from 2020")
#    KNMI_240_2023 = KNMI_240[(KNMI_240["datetime"] > pd.to_datetime("2021-01-01 21:00:00+00:00")) &
#                             (KNMI_240["datetime"] < pd.to_datetime("2022-01-01 21:00:00+00:00"))].copy()
#    windcountplot(KNMI_240_2023, True, "Windcountplot Schiphol (240) from 2021")
#    KNMI_240_2023 = KNMI_240[(KNMI_240["datetime"] > pd.to_datetime("2022-01-01 21:00:00+00:00")) &
#                             (KNMI_240["datetime"] < pd.to_datetime("2023-01-01 21:00:00+00:00"))].copy()
#    windcountplot(KNMI_240_2023, True, "Windcountplot Schiphol (240) from 2022")
#    KNMI_240_2023 = KNMI_240[KNMI_240["datetime"] > pd.to_datetime("2023-01-01 21:00:00+00:00")].copy()
#    windcountplot(KNMI_240_2023, True, "Windcountplot Schiphol (240): 20230101 - 20230901")



#    windcountplot(KNMI_225, True, "Windcountplot ijmuiden-zuidpier (225) from "+startdate+" to "+enddate)
#    windcountplot(KNMI_209, True, "Windcountplot ijmuiden-zee (209) from "+startdate+" to "+enddate)

#    KNMI_225_2023 = KNMI_225[KNMI_225["datetime"] > pd.to_datetime("2023-01-01 21:00:00+00:00")].copy()
#    windcountplot(KNMI_225, True, "Windcountplot ijmuiden-zuidpier (225): 20230101 - 20230901")
#    KNMI_209_2023 = KNMI_209[KNMI_209["datetime"] > pd.to_datetime("2023-01-01 21:00:00+00:00")].copy()
#    windcountplot(KNMI_209, True, "Windcountplot ijmuiden-zee (209): 20230101 - 20230901")

#  WINDCOUNTPLOT WITH SMOOTIFY
#    result = countvalues(KNMI_240_2023, "winddirection")
#    windplot(result, "count", title="Schiphol directions 2023, smooth = 0", smooth=0)
#    result = countvalues(KNMI_240_2023, "winddirection")
#    windplot(result, "count", title="Schiphol directions 2023, smooth = 1", smooth=1)
#    result = countvalues(KNMI_240_2023, "winddirection")
#    windplot(result, "count", title="Schiphol directions 2023, smooth = 2", smooth=2)
#    result = countvalues(KNMI_240_2023, "winddirection")
#    windplot(result, "count", title="Schiphol directions 2023, smooth = 3", smooth=3)

#  WINDSPEEDPLOTS
#    windplot(KNMI_240, "windspeed", title="Schiphol windspeed plot, smooth = 20 degrees", smooth=2)
 #   windplot(KNMI_240, "windspeed", title="Schiphol windspeed plot no smooth",smooth=0)


#   CORRELATION SCHIPHOL AND ZUIDPIER
#    dropNoWindDirection(KNMI_240_2023)
#    dropNoWindDirection(KNMI_225_2023)
#    merged = pd.merge(KNMI_240_2023, KNMI_225_2023, on="datetime", suffixes=("_Schiphol", "_IJmuiden"))
#    merged["number"] = "number"
#    result = merged.groupby(["winddirection_Schiphol", "winddirection_IJmuiden"])["number"].count()

#    scatter = sns.scatterplot(result, x="winddirection_Schiphol", y="winddirection_IJmuiden")
#    scatter.set(title="Scatterplot for 2023")
#    scatter.set(xlim=(5, 365))
#    scatter.set(ylim=(5, 365))
#    plt.show()

#   CORRELATION ZEE AND ZUIDPIER
#    dropNoWindDirection(KNMI_209_2023)
#    dropNoWindDirection(KNMI_225_2023)

#    merged = pd.merge(KNMI_209_2023, KNMI_225_2023, on="datetime", suffixes=("_Zee", "_Zuidpier"))
#    merged["number"] = "number"
#    result = merged.groupby(["winddirection_Zee", "winddirection_Zuidpier"])["number"].count()

#   scatter = sns.scatterplot(result, x="winddirection_Zee", y="winddirection_Zuidpier")
#    scatter.set(title="Scatterplot for 2023 IJmuiden")
#    scatter.set(xlim=(5, 365))
#    scatter.set(ylim=(5, 365))
#    plt.show()

#    hplot = sns.histplot(data=KNMI_240, x="winddirection",binwidth=10)
#    hplot.set(xlim=(0, 370))
    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



