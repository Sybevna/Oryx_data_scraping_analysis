# Import modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.preprocessing import cleanup, create_dfs
import pickle

#%% Open browser and navigate to page to retrieve data from
url = (
    "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
)
html = requests.get(url).content
soup = BeautifulSoup(html)
#%% Retrieve content from HTML page
# Cleanup data - to be put in separate file
# Remove all the HTML characters and things we don't need
# Split all elements into different str
tags2 = soup.find_all(
    "h3"
)  # Retrive all content of h3 tags- where data of interest is stored
data = [x.text for x in tags2 if len(x.text) > 1]
data = [cleanup(x) for x in data]

data = create_dfs(data)


df_ru, df_ua = data.values()

#%% Dump dataframes with pickle
df_ru.to_csv(r"df_ru.csv", header=True, index=None, sep=",", mode="w")
df_ua.to_csv(r"df_ua.csv", header=True, index=None, sep=",", mode="w")
#%% Create paths to save figs
path_ru = os.path.join(os.getcwd(), "Russia")
if not os.path.exists("Russia"):
    os.makedirs("Russia")

path_ua = os.path.join(os.getcwd(), "Ukraine")
if not os.path.exists("Ukraine"):
    os.makedirs("Ukraine")
#%% Stacked bar chart per vehicle


df_ru.sort_values(by=["total"], ascending=False).iloc[1:].drop(columns=["total"]).plot(
    kind="bar", stacked=True, title="Stack"
).figure.savefig("Russia/stacked_chart_Russia.jpg", bbox_inches="tight")
df_ua.sort_values(by=["total"], ascending=False).iloc[1:].drop(columns=["total"]).plot(
    kind="bar", stacked=True, title="Stack"
).figure.savefig("Ukraine/stacked_chart_Ukraine.jpg", bbox_inches="tight")

#%% Russian/Ukrainian summary - subplot
fig1, (ax2, ax3) = plt.subplots(nrows=2, ncols=1)  # two axes on figure
Tasks = df_ru.loc[0].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
ax2.pie(Tasks, labels=my_labels, autopct="%1.1f%%", textprops={"fontsize": 7})
ax2.set_title(
    df_ru.loc[0].loc["Vehicle Type"]
    + " (Total: "
    + str(df_ru.loc[0].loc["Total"])
    + ") "
)
ax2.axis("equal")
# ax2.plt.show()

Tasks_ua = df_ua.loc[0].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
ax3.pie(Tasks_ua, labels=my_labels, autopct="%1.1f%%", textprops={"fontsize": 7})
ax3.set_title(
    df_ru.loc[0].loc["Vehicle Type"]
    + " (Total: "
    + str(df_ua.loc[0].loc["Total"])
    + ") "
)
ax3.axis("equal")
# ax3.show()
fig1.savefig(os.path.join(path_ru, "Pie_chart_RU_UA.png"), bbox_inches="tight", dpi=600)

fig1, ax1 = plt.subplots()
Tasks = df_ru.loc[0].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
ax1.pie(Tasks, labels=my_labels, autopct="%1.1f%%", textprops={"fontsize": 7})
ax1.set_title(
    df_ru.loc[0].loc["Vehicle Type"]
    + " (Total: "
    + str(df_ru.loc[0].loc["Total"])
    + ") "
)
ax1.axis("equal")
fig1.savefig(os.path.join(path_ru, "Pie_chart_RU.png"), bbox_inches="tight", dpi=600)
# ax2.plt.show()

fig1, ax1 = plt.subplots()
Tasks = df_ua.loc[0].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
ax1.pie(Tasks, labels=my_labels, autopct="%1.1f%%", textprops={"fontsize": 7})
ax1.set_title(
    df_ua.loc[0].loc["Vehicle Type"]
    + " (Total: "
    + str(df_ua.loc[0].loc["Total"])
    + ") "
)
ax1.axis("equal")
fig1.savefig(os.path.join(path_ua, "Pie_chart_UA.png"), bbox_inches="tight", dpi=600)
# ax2.plt.show()
#%% Russian losses per vehicle type

for i in range(1, len(df_ru)):
    fig1, ax1 = plt.subplots()
    m2 = (df_ru.iloc[[i]] != 0).any()
    m1 = df_ru.columns[m2][2:]
    # Tasks = df_ru.loc[i].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
    Tasks = df_ru.loc[i].loc[m1]
    # my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
    ax1.pie(
        Tasks, labels=m1, autopct=lambda p: "{:.1f}%".format(round(p)) if p > 0 else ""
    )
    ax1.set_title(
        df_ru.loc[i].loc["Vehicle Type"]
        + " (Total: "
        + str(df_ru.loc[i].loc["Total"])
        + ") - Russia"
    )
    ax1.axis("equal")
    # plt.show()
    fig1.savefig(
        os.path.join(
            path_ru, "Pie_chart_RU_" + df_ru.loc[i].loc["Vehicle Type"] + ".png"
        ),
        bbox_inches="tight",
        dpi=600,
    )

for i in range(1, len(df_ua)):
    fig1, ax1 = plt.subplots()
    # Tasks = df_ua.loc[i].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
    m2 = (df_ru.iloc[[i]] != 0).any()
    m1 = df_ru.columns[m2][2:]
    # Tasks = df_ru.loc[i].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
    Tasks = df_ru.loc[i].loc[m1]
    my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
    ax1.pie(
        Tasks,
        labels=m1,
        autopct=lambda p: "{:.1f}%".format(round(p)) if p > 0 else "",
        textprops={"fontsize": 7},
    )
    ax1.set_title(
        df_ua.loc[i].loc["Vehicle Type"]
        + " (Total: "
        + str(df_ua.loc[i].loc["Total"])
        + ") - Ukraine"
    )
    ax1.axis("equal")
    # plt.show()
    fig1.savefig(
        os.path.join(
            path_ua, "Pie_chart_UA_" + df_ua.loc[i].loc["Vehicle Type"] + ".png"
        ),
        bbox_inches="tight",
        dpi=600,
    )

#%%
