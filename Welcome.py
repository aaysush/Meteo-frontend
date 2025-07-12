import streamlit as st 
import pandas as pd
import numpy as np
import requests

st.set_page_config(
    page_icon="⛈️",
    page_title='main page'

)

st.title('Meteorological Data Forecasting and Insights')

#st.header('**What we offer ?**')


st.divider()

st.subheader('**Get Real Time data and analysis of factors like**')

st.write("""
❄️ Temperature: Know the real-time temperature and how it feels with our apparent temperature insights.\n

❄️ Dewpoint & Humidity: Understand atmospheric moisture with relative humidity and dewpoint measurements.\n

❄️ Wind Speed & Direction: Stay ahead with wind forecasts and directional analysis.\n
❄️ Cloud Cover: See how the skies will unfold with average cloud coverage updates.

❄️ Rainfall: Be prepared with precise precipitation forecasts.\n

❄️ Pressure: Track surface and sea-level pressure for a full atmospheric perspective.\n

❄️ Visibility: Plan better with visibility levels for clear navigation.\n

❄️ UV Index: Stay safe with insights into UV exposure throughout the day.\n

❄️ Chance of Rain: Don’t let surprise showers catch you off guard.\n

❄️ Vapour Pressure Deficit: Perfect for agriculture and understanding plant stress.\n""")

st.divider()



st.subheader('**We don’t just show you the present; We take you into the future!**')
st.write('**here we forecast meteorological factors like...**')


with st.container(border = True):

 pred1 , pred2 ,pred3 =st.columns(3)

with pred1:
    st.header('Temperature 🌤️')
    st.write('Know how the weather will shift in the coming hours—stay prepared, no surprises.')


with pred2:
    st.header('Humidity ☁️')
    st.write('We predict the moisture levels so you can plan for comfort or productivity.')

with pred3 :
    st.header('Rainfall Probabilty 🌧️')
    st.write(' Wondering about a drizzle or a downpour? Our rainfall forecasts have you covered, helping you make smarter choices.')




