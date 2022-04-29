import requests
from bs4 import BeautifulSoup
import streamlit as st


from utils.preprocessing import cleanup, create_dfs


def scrap():
    url = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
    url2 = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-ukrainian.html"
    html = requests.get(url).content
    html2 = requests.get(url2).content
    soup = BeautifulSoup(html)
    soup2 = BeautifulSoup(html2)
    #%% Retrieve content from HTML page
    # Cleanup data - to be put in separate file
    # Remove all the HTML characters and things we don't need
    # Split all elements into different str
    tags2 = soup.find_all(
        "h3"
    )  # Retrive all content of h3 tags- where data of interest is stored
    tags3 = soup2.find_all(
        "h3"
    ) 
    data = [x.text for x in tags2 if len(x.text) > 1]
    data = [cleanup(x) for x in data]
    data2 = [x.text for x in tags3 if len(x.text) > 1]
    data2 = [cleanup(x) for x in data2]
    data = data+data2
    data = create_dfs(data)
    return data
