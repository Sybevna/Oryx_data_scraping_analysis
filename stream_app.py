#%% Import modules
import streamlit as st
import pickle
import pandas as pd
import os
from PIL import Image
from itertools import cycle
import matplotlib.pyplot as plt
from func_stream import scrap, pie_maker,disp_buttons
from datetime import datetime
#%% Define paths
path_ru = os.path.join(os.getcwd(), "Russia")
path_ua = os.path.join(os.getcwd(), "Ukraine")
#%% Import dataframes
#df_ru = pd.read_csv('df_ru.csv',index_col = 0)
#df_ua = pd.read_csv('df_ua.csv',index_col = 0)

#%% datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
str_date = "scrapping done at: "+ dt_string
#%% Call scraping function
df_ru, df_ua = scrap()
#%%
st.title('Attack On Europe: Documenting Equipment Losses During The 2022 Russian Invasion Of Ukraine: [Source](https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html)')
st.text(str_date)
st.header("Summary", anchor=None)
#%% Generate Russian/Ukrainian summary
fig1, (ax2, ax3) = plt.subplots(nrows=2, ncols=1)  # two axes on figure
Tasks = df_ru.iloc[0].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
ax2.pie(Tasks, labels=my_labels, autopct="%1.1f%%", textprops={"fontsize": 7})
ax2.set_title(
    df_ru.index[0]
    + " (Total: "
    + str(df_ru.iloc[0]["Total"])
    + ") "
)
ax2.axis("equal")
# ax2.plt.show()

Tasks_ua = df_ua.iloc[0].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
ax3.pie(Tasks_ua, labels=my_labels, autopct="%1.1f%%", textprops={"fontsize": 7})
ax3.set_title(
    df_ua.index[0]
    + " (Total: "
    + str(df_ua.iloc[0]["Total"])
    + ") "
)
ax3.axis("equal")
# ax3.show()
fig1.savefig(os.path.join(path_ru, "Pie_chart_RU_UA.png"), bbox_inches="tight", dpi=600)
#%% Display summary graph
#image1 = Image.open(os.path.join(path_ru, "Pie_chart_RU_UA.png"))
#st.image([image1, image2], width=150, use_column_width = True)
#st.image([image1], width=150, use_column_width = True)

st.pyplot(fig = fig1)
#%% Vehicle summary graphs summary 
st.subheader("Summary by type of vehicles", anchor=None)

df_ru.sort_values(by=["Total"], ascending=False).iloc[1:].drop(columns=["Total"]).plot(
    kind="bar", stacked=True, title="Russia"
).figure.savefig("Russia/stacked_chart_Russia.png", bbox_inches="tight")
df_ua.sort_values(by=["Total"], ascending=False).iloc[1:].drop(columns=["Total"]).plot(
    kind="bar", stacked=True, title="Ukraine"
).figure.savefig("Ukraine/stacked_chart_Ukraine.png", bbox_inches="tight")
#%% Display vehicle summary graphs
image1 = Image.open(os.path.join(path_ru, "stacked_chart_Russia.png"))
image2 = Image.open(os.path.join(path_ua, "stacked_chart_Ukraine.png"))
#st.image([image1, image2], width=150, use_column_width = True)

filteredImages = [image1, image2] # your images here
caption = ["", ""] # your caption here
cols = cycle(st.columns(2)) # st.columns here since it is out of beta at the time I'm writing this
for idx, filteredImage in enumerate(filteredImages):
    next(cols).image(filteredImage, width=335, caption=caption[idx])

#   st.pyplot(fig = fig1)

st.subheader("Generate a specific graph:", anchor=None)
 
option = st.selectbox("Country ",("Russia","Ukraine"))
if option == "Russia":
    disp_buttons(df_ru)
else:
    disp_buttons(df_ru)
    #button_RU.empty()
    
 

    