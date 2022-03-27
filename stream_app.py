#%% Import modules
from pyparsing import col
import streamlit as st
from datetime import datetime

from utils.plot_creation import summary, pie_plot, summary_type
from utils.scraping import scrap


def main():
    #%% datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    str_date = "scrapping done at: " + dt_string
    #%% Call scraping function
    data = scrap()
    #%%
    st.title(
        "Attack On Europe: Documenting Equipment Losses During The 2022 Russian Invasion Of Ukraine: [Source](https://www.oryxspioenkop.com/2022/02/attack-on-europe-documenting-equipment.html)"
    )
    st.text(str_date)
    st.header("Summary", anchor=None)

    st.pyplot(fig=summary(data))
    st.subheader("Summary by type of vehicles", anchor=None)

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(summary_type(data, "Russia"))

    with col2:
        st.pyplot(summary_type(data, "Ukraine"))
    return data


def following(data):
    st.subheader("Generate a specific graph:", anchor=None)
    col3, col4 = st.columns(2)
    with col3:
        country = st.selectbox("Country", ("Russia", "Ukraine"))
    with col4:
        equipement = st.selectbox("Type", data[country].iloc[1:].index.values)
    return [country, equipement]


def specific(data, country, equipement):
    st.write(pie_plot(data, country=country, equipement=equipement))


if __name__ == "__main__":
    data = main()
    country, equipement = following(data)
    specific(data, country, equipement)
