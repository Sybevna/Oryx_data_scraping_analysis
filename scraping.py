# Import modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.preprocessing import cleanup
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
Data = [x.text for x in tags2 if len(x.text) > 1]
Data = [cleanup(x) for x in Data]

#%% Put all rows in same format
# This handles cases where all the categories are not all present, or 2 are present, or 3 etc...
# The idea is to standardise the format of the data to put everything in DF after

for i in range(len(Data)):
    if (
        "captured" in Data[i]
        and "destroyed" not in Data[i]
        and "damaged" not in Data[i]
        and "abandoned" not in Data[i]
    ):
        j = Data[i].index("captured")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = (
            temp1
            + ["destroyed"]
            + [" 0 "]
            + ["damaged "]
            + ["0 "]
            + ["abandoned "]
            + ["0 "]
            + temp2
        )
        continue

    if (
        "abandoned" in Data[i]
        and "destroyed" not in Data[i]
        and "damaged" not in Data[i]
        and "captured" not in Data[i]
    ):
        j = Data[i].index("abandoned")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = (
            temp1
            + ["destroyed"]
            + [" 0 "]
            + ["damaged "]
            + ["0 "]
            + temp2
            + ["captured "]
            + ["0 "]
        )
        continue

    if (
        "damaged" in Data[i]
        and "destroyed" not in Data[i]
        and "abandoned" not in Data[i]
        and "captured" not in Data[i]
    ):
        j = Data[i].index("damaged")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = (
            temp1
            + ["destroyed"]
            + [" 0 "]
            + temp2
            + ["abandoned "]
            + ["0 "]
            + ["captured "]
            + ["0 "]
        )
        continue

    if (
        "destroyed" in Data[i]
        and "damaged" not in Data[i]
        and "abandoned" not in Data[i]
        and "captured" not in Data[i]
    ):
        j = Data[i].index("destroyed")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = (
            temp1
            + temp2
            + ["damaged "]
            + ["0 "]
            + ["abandoned "]
            + ["0 "]
            + ["captured "]
            + ["0 "]
        )
        continue
        ## 2 out of 4
    if (
        "destroyed" not in Data[i]
        and "damaged" not in Data[i]
        and "abandoned" in Data[i]
        and "captured" in Data[i]
    ):
        j = Data[i].index("abandoned")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = temp1 + ["destroyed"] + [" 0 "] + ["damaged "] + ["0 "] + temp2
        continue

    if (
        "destroyed" not in Data[i]
        and "damaged" in Data[i]
        and "abandoned" in Data[i]
        and "captured" not in Data[i]
    ):
        j = Data[i].index("damaged")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = temp1 + ["destroyed"] + ["0 "] + temp2 + ["captured "] + ["0 "]
        continue

    if (
        "destroyed" in Data[i]
        and "damaged" in Data[i]
        and "abandoned" not in Data[i]
        and "captured" not in Data[i]
    ):
        Data[i] = Data[i] + ["abandoned "] + ["0 "] + ["captured "] + ["0 "]
        continue

    if (
        "destroyed" in Data[i]
        and "damaged" not in Data[i]
        and "abandoned" in Data[i]
        and "captured" not in Data[i]
    ):
        j = Data[i].index("abandoned")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = temp1 + ["damaged "] + ["0 "] + temp2 + ["captured "] + ["0 "]
        continue

    if (
        "destroyed" in Data[i]
        and "damaged" not in Data[i]
        and "abandoned" not in Data[i]
        and "captured" in Data[i]
    ):
        j = Data[i].index("captured")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = temp1 + ["damaged "] + ["0 "] + ["abandoned "] + ["0 "] + temp2
        continue

    if (
        "destroyed" not in Data[i]
        and "damaged" in Data[i]
        and "abandoned" not in Data[i]
        and "captured" in Data[i]
    ):
        j = Data[i].index("damaged")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j : j + 2]
        temp3 = Data[i][j + 2 :]
        Data[i] = (
            temp1 + ["destroyed"] + [" 0 "] + temp2 + ["abandoned "] + ["0 "] + temp3
        )
        continue

    if (
        "destroyed" not in Data[i]
        and "damaged" in Data[i]
        and "abandoned" in Data[i]
        and "captured" in Data[i]
    ):
        j = Data[i].index("damaged")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = temp1 + ["destroyed"] + temp2
        continue

    if (
        "destroyed" in Data[i]
        and "damaged" in Data[i]
        and "abandoned" in Data[i]
        and "captured" not in Data[i]
    ):
        j = Data[i].index("damaged")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = Data[i] + ["captured "] + ["0 "]
        continue

    if (
        "destroyed" in Data[i]
        and "damaged" in Data[i]
        and "abandoned" not in Data[i]
        and "captured" in Data[i]
    ):
        j = Data[i].index("captured")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = temp1 + ["abandoned "] + ["0 "] + temp2
        continue

    if (
        "destroyed" in Data[i]
        and "damaged" not in Data[i]
        and "abandoned" in Data[i]
        and "captured" in Data[i]
    ):
        j = Data[i].index("abandoned")
        temp1 = Data[i][0:j]
        temp2 = Data[i][j:]
        Data[i] = temp1 + ["damaged "] + ["0 "] + temp2
        continue

#%% Collapse names in 1 str for long vehicle names
for i in range(len(Data)):
    j = Data[i].index("destroyed")
    Data[i] = [" ".join(Data[i][: j - 1])] + Data[i][
        j - 1 :
    ]  # Use j-1 to point grab everything BEFORE the total number for each category
    if "Ukraine" in Data[i]:
        k = i
#%% Get everything into Pandas Dataframe - split into 2 dataframes for each country
df_ru = pd.DataFrame(
    Data[:k],
    columns=[
        "Vehicle Type",
        "Total",
        "des",
        "Destroyed",
        "dam",
        "Damaged",
        "aba",
        "Abandoned",
        "capt",
        "Captured",
    ],
)
df_ua = pd.DataFrame(
    Data[k:],
    columns=[
        "Vehicle Type",
        "Total",
        "des",
        "Destroyed",
        "dam",
        "Damaged",
        "aba",
        "Abandoned",
        "capt",
        "Captured",
    ],
)
#%% Convert columns to numeric
df_ru.Total = pd.to_numeric(df_ru.Total)
df_ru.Destroyed = pd.to_numeric(df_ru.Destroyed)
df_ru.Damaged = pd.to_numeric(df_ru.Damaged)
df_ru.Abandoned = pd.to_numeric(df_ru.Abandoned)
df_ru.Captured = pd.to_numeric(df_ru.Captured)

df_ua.Total = pd.to_numeric(df_ua.Total)
df_ua.Destroyed = pd.to_numeric(df_ua.Destroyed)
df_ua.Damaged = pd.to_numeric(df_ua.Damaged)
df_ua.Abandoned = pd.to_numeric(df_ua.Abandoned)
df_ua.Captured = pd.to_numeric(df_ua.Captured)

# df_ua.replace(0, np.nan, inplace=True)
# df_ru.replace(0, np.nan, inplace=True)
#%% Get rid of columns with same words - tidy up
df_ru = df_ru.drop(labels=["des", "dam", "aba", "capt"], axis=1)
df_ua = df_ua.drop(labels=["des", "dam", "aba", "capt"], axis=1)
#%% Dump dataframes with pickle
df_ru.to_csv(r'df_ru.csv', header=True, index=None, sep=',', mode='w')
df_ua.to_csv(r'df_ua.csv', header=True, index=None, sep=',', mode='w')
#%% Create paths to save figs
path_ru = os.path.join(os.getcwd(), "Russia")
if not os.path.exists("Russia"):
    os.makedirs("Russia")

path_ua = os.path.join(os.getcwd(), "Ukraine")
if not os.path.exists("Ukraine"):
    os.makedirs("Ukraine")
#%% Stacked bar chart per vehicle
ax = df_ru.sort_values(by = "Total",ascending = False).iloc[1:].plot.bar(
    x="Vehicle Type",
    y=["Destroyed", "Damaged", "Abandoned", "Captured"],
    stacked=True,
    title="Russia",
    grid=True,
)  # bar chart RU
ax.figure.savefig(
    os.path.join(path_ru, "stacked_chart_Russia.png"), bbox_inches="tight", dpi=600
)
ax1 = df_ua.sort_values(by = "Total",ascending = False).iloc[1:].plot.bar(
    x="Vehicle Type",
    y=["Destroyed", "Damaged", "Abandoned", "Captured"],
    stacked=True,
    title="Ukraine",
    grid=True,
)  # bar chart UA
ax1.figure.savefig(
    os.path.join(path_ua, "stacked_chart_Ukraine.png"), bbox_inches="tight", dpi=600
)

#%% Russian/Ukrainian summary - subplot
fig1, (ax2, ax3) = plt.subplots(nrows=2, ncols=1)  # two axes on figure
Tasks = df_ru.loc[0].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
ax2.pie(Tasks, labels=my_labels, autopct="%1.1f%%",textprops={'fontsize': 7})
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
ax3.pie(Tasks_ua, labels=my_labels, autopct="%1.1f%%",textprops={'fontsize': 7})
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
ax1.pie(Tasks, labels=my_labels, autopct="%1.1f%%",textprops={'fontsize': 7})
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
ax1.pie(Tasks, labels=my_labels, autopct="%1.1f%%",textprops={'fontsize': 7})
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
        Tasks, labels=m1, autopct=lambda p: "{:.1f}%".format(round(p)) if p > 0 else ""
    ,textprops={'fontsize': 7})
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
