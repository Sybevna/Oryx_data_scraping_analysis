import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


def summary(data):
    for country in data.keys():
        test = data[country].iloc[0]
        if country == "Russia":
            plt.subplot(211)
        else:
            plt.subplot(212)
        plt.pie(
            test[1:],
            autopct="%1.1f%%",
            textprops={"fontsize": 7},
            labels=test[1:].index,
        )
        plt.title(f"{test.name} (total: {test.Total}) - {country}")
    return plt


def pie_plot(data, country, equipement):
    DATA = data[country].drop(columns=["Total"]).T

    fig = go.Figure(
        go.Pie(
            values=DATA[equipement].values,
            labels=DATA[equipement].index.values,
            title=f"{equipement} (total: {data[country].loc[equipement].Total}) - {country}",
        )
    )
    return fig


def summary_type(data, country):
    return (
        data[country]
        .sort_values(by=["Total"], ascending=False)
        .iloc[1:]
        .drop(columns=["Total"])
        .plot(kind="bar", stacked=True, title=f"Total - {country}")
        .figure
    )
