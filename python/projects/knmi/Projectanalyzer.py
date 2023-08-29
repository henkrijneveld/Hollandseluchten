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

KNMI_240 = pd.DataFrame()
startdate = "20200101"
enddate = "20230801"
projectdir = "/home/henk/Projects/Hollandseluchten/python/projects/knmi"

def runit():
    setGlobalPlot()

    windhistogram(KNMI_240, False)
#    hplot = sns.histplot(data=KNMI_240, x="winddirection",binwidth=10)
#    hplot.set(xlim=(0, 370))
    plt.show()
    return


# run stand alone entry point
if __name__ == '__main__':
#    pd.options.mode.copy_on_write = True
#    printGlobals(os.getcwd())
    importDataframes(os.getcwd(), globals())
    runit()



