import requests
from bs4 import BeautifulSoup
import streamlit as st


from utils.preprocessing import cleanup, create_dfs


def scrap():
    url = "https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html"
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
    return data
