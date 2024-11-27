import os
os.system('pip install pandas streamlit numpy duckduckgo-search requests')

import pandas as pd
import streamlit as st
import numpy as np
import requests
from duckduckgo_search import DDGS


data = pd.read_csv("https://raw.githubusercontent.com/cruzdariel/Airport-Fare-Dashboard/refs/heads/main/cleanairline.csv")

def fetch_first_image(query):
    with DDGS() as ddgs:
        results = ddgs.images(query, max_results=1)
        if results:
            url = results[0]['image']
            response = requests.head(url)
            if response.status_code == 200:
                return url
            else:
                return None
        return None

st.title("Average Airline Fare by Airport")

airport = st.selectbox("Select an Airport:", data["Airport Name"])

airport_data = data[data["Airport Name"] == airport]

if not airport_data.empty:
    fare = airport_data["Average Fare ($)"].values[0]
    st.write(f"### Average Fare: ${fare:.2f}")
    national_average = data["Average Fare ($)"].mean()
    percent_difference = ((fare - national_average) / national_average) * 100
    if percent_difference > 0:
        st.write(f"#### That's {percent_difference:.2f}% <span style='color:red;'>higher</span> than the national average.", unsafe_allow_html=True)
    else:
        st.write(f"#### That's {np.abs(percent_difference):.2f}% <span style='color:green;'>lower</span>  than the national average.", unsafe_allow_html=True)

else:
    st.write("No data available for the selected airport.")

image_url = fetch_first_image(airport)

if image_url:
    st.image(image_url, caption=f"Image of {airport}, sourced from {image_url}")
else:
    st.write("No image available for this airport.")

st.write("*Data Source:* https://www.transtats.bts.gov/AverageFare/")
#if st.checkbox("Show Full Data"):
  #  st.dataframe(data)