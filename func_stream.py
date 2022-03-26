# Support function for the streamlit dashboard
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils.preprocessing import cleanup, create_dfs
import streamlit as st
def scrap():
    # Open browser and navigate to page to retrieve data from
    url = (
        "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
    )
    html = requests.get(url).content
    soup = BeautifulSoup(html)
    # Retrieve content from HTML page
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
    df_ru.rename(columns= {"destroyed":"Destroyed","damaged":"Damaged", "abandoned":"Abandoned","captured":"Captured"},inplace = True)
    df_ua.rename(columns= {"destroyed":"Destroyed","damaged":"Damaged", "abandoned":"Abandoned","captured":"Captured"}, inplace= True)
    
    return df_ru, df_ua

    
def pie_maker(df):
     fig1, ax1 = plt.subplots()
     m2 = (df != 0)
     m1 = df[m2][1:].index
     # Tasks = df_ru.loc[i].loc[["Destroyed", "Damaged", "Abandoned", "Captured"]]
     Tasks = df.loc[m1]
     # my_labels = ["Destroyed", "Damaged", "Abandoned", "Captured"]
     ax1.pie(
         Tasks, labels=m1, autopct=lambda p: "{:.1f}%".format(round(p)) if p > 0 else ""
     )
     #ax1.set_title(
         #df.index
        # + " (Total: "
         #+ str(df.loc["Total"])
         #+ ") - Russia"
    # )
     ax1.axis("equal")
     st.pyplot(fig = fig1)
      
     
def disp_buttons(df):
    for i in range(1, len(df)):
        #st.button(df.loc[i].loc["Vehicle Type"], key=i, help=None )   
        if st.button(df.index[i], key=i, help=None):
            pie_maker(df.iloc[i])
           #pie_maker(df.iloc[i])