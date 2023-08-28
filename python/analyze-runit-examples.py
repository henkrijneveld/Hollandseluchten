def runit():
    setGlobalPlot()
    merged = pd.merge(NL49701, NL49704, on='datetime', suffixes=("_first", "_last"))
    merged["delta_pm"] = merged.apply(lambda x: x["pm25_first"] - x["pm25_last"], axis=1)
    deltas = pd.DataFrame()
    deltas["delta_pm"] = merged["delta_pm"].copy()
    deltas.sort_values(inplace=True, ignore_index=True, by="delta_pm")
    lplot = sns.histplot(data=deltas, x="delta_pm", binwidth=0.20, kde=True)
    lplot.set(xlim=(-50.0, 50.0))
    return

    # dataframe met temperatuurverschil 545 en 549
    merged = pd.merge(NL49570, HLL_549, on='datetime', suffixes=("_545", "_549"))
#    merged["delta_temperature"] = merged.apply(lambda x: x["temperature_545"] - x["temperature_549"], axis=1)#
    merged["delta_pm"] = merged.apply(lambda x: x["pm25_545"] - x["pm25_549"], axis=1)#
#    sns.lineplot(merged, x="datetime", y="delta_temperature")

    deltas = pd.DataFrame()
#    deltas["delta_temperature"] = merged["delta_temperature"].copy()
    deltas["delta_pm"] = merged["delta_pm"].copy()
 #   deltas.sort_values(inplace=True, ignore_index=True, by="delta_temperature")
#    sns.histplot(data=deltas, x="delta_temperature", binwidth=0.05)
    deltas.sort_values(inplace=True, ignore_index=True, by="delta_pm")
    lplot = sns.histplot(data=deltas, x="delta_pm", binwidth=0.05, ax=ax)
    lplot.set(xlim=(-50.0, 50.0))
    smootifyLineplot(lplot)

    return

    merged = pd.merge(OZK_1850, OZK_1845, on='datetime', suffixes=("_1850", "_1845"))

    concat = pd.concat([OZK_1850, OZK_1845, HLL_545, HLL_549], ignore_index=True)
    concat = pd.merge(concat, NL49570, on='datetime', suffixes=("", "_NL"))
    concat["pm25_difference"] = concat.apply(lambda row: row["pm25_NL"] - row["pm25"], axis=1)

    # concat = concat[concat["datetime"] < mindate]

#    sns.lineplot(concat, x = "datetime",y = "pm25_difference", hue="sensorname")

#    relplot = sns.relplot(data=concat, kind="line", x="datetime", y="pm25_difference", col="sensorname",
#                hue="sensorname", col_wrap=2, palette="rocket")

#     smootifyRelplot(relplot)

    mean_545 = HLL_545
    mean_545["datetime"] = mean_545["datetime"].dt.floor("D")
    mean_545 = mean_545.groupby(by=["datetime"]).mean(numeric_only=True)
    mean_545["sensorname"] = "HLL_545"

    mean_240 = KNMI_240
    mean_240["datetime"] = mean_240["datetime"].dt.floor("D")
    mean_240 = mean_240.groupby(by=["datetime"]).mean(numeric_only=True)
    mean_240["sensorname"] = "KNMI_240"


    merged = pd.concat([mean_545, mean_240])

#    lplot = sns.histplot(data=merged, x="datetime", y="temperature_545", binwidth=1)
    lplot = sns.histplot(data=merged, x="datetime", y="temperature", hue="sensorname", multiple="dodge", binwidth=1)

    lplot.set(xlim=(convertToDatetime("20230501"), convertToDatetime("20230520")))
    smootifyLineplot(lplot)
    printf("todo some things\n")

