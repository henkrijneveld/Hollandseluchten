# seaborn dataplot library test

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import datetime

import sys
def printf(format, *args):
    sys.stdout.write(format % args)


def runit():
    dots = sns.load_dataset("dots")
    sns.relplot(
        data=dots, kind="line",
        x="time", y="firing_rate", col="align",
        hue="choice", size="coherence", style="choice",
        facet_kws=dict(sharex=False),
    )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runit()
    plt.show()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
