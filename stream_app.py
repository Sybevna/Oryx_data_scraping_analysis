#%% Import modules
import streamlit as st
import pickle
import pandas as pd
import os
from PIL import Image
from itertools import cycle
import matplotlib.pyplot as plt
#%% Define paths
path_ru = os.path.join(os.getcwd(), "Russia")
path_ua = os.path.join(os.getcwd(), "Ukraine")
#%% Import dataframes
df_ru = pd.read_csv('df_ru.csv')
df_ua = pd.read_csv('df_ru.csv')
#%%
st.title('Attack On Europe: Documenting Equipment Losses During The 2022 Russian Invasion Of Ukraine')

st.header("Summary", anchor=None)
image1 = Image.open(os.path.join(path_ru, "Pie_chart_RU_UA.png"))
#st.image([image1, image2], width=150, use_column_width = True)
st.image([image1], width=150, use_column_width = True)


#%% Vehicle summary
st.subheader("Summary by type of vehicles", anchor=None)


image1 = Image.open(os.path.join(path_ru, "stacked_chart_Russia.png"))
image2 = Image.open(os.path.join(path_ua, "stacked_chart_Ukraine.png"))
#st.image([image1, image2], width=150, use_column_width = True)


filteredImages = [image1, image2] # your images here
caption = ["im1", "im2"] # your caption here
cols = cycle(st.columns(2)) # st.columns here since it is out of beta at the time I'm writing this
for idx, filteredImage in enumerate(filteredImages):
    next(cols).image(filteredImage, width=335, caption=caption[idx])
    
def pie_maker(df):
     fig1, ax1 = plt.subplots(1,1,figsize=(10,4))
     m2 = (df != 0).any()
     m1 = df.columns[m2][2:]
     # Tasks = df_ru.loc[i].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
     Tasks = df.loc[m1]
     # my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
     ax1.pie(
         Tasks, labels=m1, autopct=lambda p: "{:.1f}%".format(round(p)) if p > 0 else ""
     )
     ax1.set_title(
         df.loc["Vehicle Type"]
         + " (Total: "
         + str(df_ru.loc["Total"])
         + ")"
     )
     ax1.axis("equal")
     st.pyplot(fig = fig1, clear_figure  = False)
     
     
def disp_buttons(df):
    for i in range(1, len(df)):
        #st.button(df.loc[i].loc["Vehicle Type"], key=i, help=None )   
        if st.button(df.loc[i].loc["Vehicle Type"], key=i, help=None ):
           pie_maker(df.loc[i])
           st.subheader("TEST", anchor=None)
    return df
            
           # clicked.empty()
            
       
    
st.subheader("Generate a specific graph:", anchor=None)
 
if st.button("Russia"):
    disp_buttons(df_ru)
    #button_RU.empty()
    
 
if st.button("Ukraine"):
    disp_buttons(df_ua)
    #button_UA.empty()
    