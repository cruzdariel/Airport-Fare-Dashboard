import pandas as pd
import streamlit as st
import numpy as np
import requests
from duckduckgo_search import DDGS

# Wed Nov 27

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

st.title("Average Airfare by Domestic Airport")

airport = st.selectbox("Select an Airport:", data["Airport Name"])
year = st.selectbox("Select a year:", options=list(range(2000, 2025)), index=24)

airport_data = data[data["Airport Name"] == airport]

st.divider()

if not airport_data.empty:
    fare = airport_data[str(year)].values[0]
    st.markdown(f"###  <span style='color:#4284f5;'>{str(airport)}</span> in  <span style='color:#4284f5;'>{airport_data['City Name'].values[0]}, {airport_data['State Name'].values[0]}</span> had an average fare in <span style='color:#4284f5;'>{str(year)}</span> of: ${fare:.2f}", unsafe_allow_html=True)
    national_average = data[str(year)].mean()
    percent_difference = ((fare - national_average) / national_average) * 100
    if percent_difference > 0:
        st.write(f"#### That's {percent_difference:.2f}% <span style='color:red;'>higher</span> than the national average.", unsafe_allow_html=True)
    else:
        st.write(f"#### That's {np.abs(percent_difference):.2f}% <span style='color:green;'>lower</span> than the national average.", unsafe_allow_html=True)

else:
    st.write("No data available for the selected airport.")

airport_data.columns = airport_data.columns.map(str)
years = [col for col in airport_data.columns if col.isdigit()]
historical_data = airport_data.melt(id_vars=['Airport Code', 'Airport Name', 'City Name'], 
                        value_vars=years, 
                        var_name='Year', 
                        value_name='Average Fare (USD)')
overall_mean = data.melt(id_vars=['Airport Code', 'Airport Name', 'City Name'], 
                         value_vars=years, 
                         var_name='Year', 
                         value_name='Average Fare (USD)').groupby('Year')['Average Fare (USD)'].mean().reset_index()

historical_data = historical_data.merge(overall_mean, on='Year', suffixes=('', ' National'))

st.line_chart(historical_data.set_index('Year')[['Average Fare (USD)', 'Average Fare (USD) National']])

image_url = fetch_first_image(airport)
if image_url:
    st.image(image_url, caption=f"Image of {airport}, sourced from {image_url} via DuckDuckGo. Image may be subject to copyright and/or may not be a correct image.")
else:
    st.write()

st.write("**Date Source:** *U.S. Department of Transportation, Bureau of Transportation Statistics* https://www.transtats.bts.gov/AverageFare/")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div.embeddedAppMetaInfoBar_container__DxxL1 {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# DCR