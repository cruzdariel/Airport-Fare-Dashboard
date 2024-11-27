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
year = st.slider("Select a year:", min_value=2014, max_value=2024, value=2024, step=1)

airport_data = data[data["Airport Name"] == airport]

st.divider()

if not airport_data.empty:
    fare = airport_data[year].values[0]
    st.write(f"### Average {year} Fare: ${fare:.2f}")
    national_average = data["Average Fare ($)"].mean()
    percent_difference = ((fare - national_average) / national_average) * 100
    if percent_difference > 0:
        st.write(f"#### That's {percent_difference:.2f}% <span style='color:red;'>higher</span> than the national average.", unsafe_allow_html=True)
    else:
        st.write(f"#### That's {np.abs(percent_difference):.2f}% <span style='color:green;'>lower</span>  than the national average.", unsafe_allow_html=True)

else:
    st.write("No data available for the selected airport.")

airport_data.columns = airport_data.columns.map(str)
years = [col for col in airport_data.columns if col.isdigit()]
historical_data = airport_data.melt(id_vars=['Airport Code', 'Airport Name', 'City Name'], 
                        value_vars=years, 
                        var_name='Year', 
                        value_name='Average Fare')
st.line_chart(historical_data, x="Year", y="Average Fare (USD, adjusted for 2024 inflation)")


st.write("**Date Source:** *U.S. Department of Transportation, Bureau of Transportation Statistics* https://www.transtats.bts.gov/AverageFare/")

image_url = fetch_first_image(airport)
if image_url:
    st.image(image_url, caption=f"Image of {airport}, sourced from {image_url}")
else:
    st.write("No image available for this airport.")

