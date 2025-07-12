import streamlit as st
import pandas as pd
import numpy as np
import requests
import logging
import os
from datetime import timedelta

# Logging setup
logging.basicConfig(level=logging.INFO)

st.set_page_config(
    page_icon="⛈️",
    page_title='Analysis & Prediction'
)

st.title('Analysis & Prediction')
st.divider()

# Sidebar Section
st.sidebar.header('Get Started by entering your region')
sidebar_latitude = st.sidebar.text_input('Enter Latitude')
sidebar_longitude = st.sidebar.text_input('Enter Longitude')

if sidebar_latitude and sidebar_longitude:
    st.sidebar.write(f"You entered:\n- **Latitude:** {sidebar_latitude}\n- **Longitude:** {sidebar_longitude}")
else:
    st.sidebar.write("Please enter both latitude and longitude in the sidebar.")

result_df = pd.DataFrame()

get_results = st.sidebar.button(f'Get results for Latitude: {sidebar_latitude} and Longitude: {sidebar_longitude}')

if get_results:
    data = {"latitude": sidebar_latitude, "longitude": sidebar_longitude}
    try:
        secret_api_key_to_talk_to_frontend_from_user_frontend = 'meteobfsecretkey'
        headers = {"secret_api_key_to_talk_to_frontend_from_user_frontend": secret_api_key_to_talk_to_frontend_from_user_frontend}
        backend_url = "http://ec2-3-108-51-226.ap-south-1.compute.amazonaws.com/process-data"

        logging.info(f"Sending request to backend: {backend_url} with data: {data}")
        response = requests.post(backend_url, json=data, headers=headers)
        logging.info(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            st.sidebar.success('Check the Analysis & Prediction tab for results.')
            result_data = response.json()
            result_df = pd.DataFrame(result_data)

            if not result_df.empty and "datetime" in result_df.columns:
                try:
                    result_df['datetime'] = pd.to_datetime(result_df['datetime'])
                    st.success("Datetime column successfully converted to datetime objects!")
                except Exception as e:
                    st.error(f"Error converting datetime column: {e}")
                    logging.exception("Failed to convert datetime column.")

            logging.info(f"Received data: {result_df.head()}")
        else:
            st.sidebar.error('There was an error. Please try again.')
            logging.error(f"Error response: {response.text}")
    except Exception as e:
        st.error(f'Process Failed: {e}')
        logging.exception("Exception occurred during API call.")

st.title('Fetched Data')
if result_df.empty:
    st.warning("No data available. Please fetch results first.")
else:
    st.dataframe(result_df)

    df = result_df.copy()

    data = {
        "Original Columns": [
            "datetime", "temperature_2m", "dewpoint_2m", "apparent_temperature",
            "wind_speed_10m", "wind_direction", "cloud_cover_avg", "surface_pressure",
            "sealevel_pressure", "rainfall", "snowfall", "relative_humidity_2m",
            "visibility", "uv_index", "chance_of_rain", "weather_condition",
            "vapour_pressure_deficit"
        ],
        "User-Friendly Names": [
            "Datetime", "Temperature (2m above surface)", "Dew Point (2m above surface)", "Feels Like Temperature",
            "Wind Speed (10m above surface)", "Wind Direction", "Cloud Cover (Avg)", "Surface Pressure",
            "Sea Level Pressure", "Rainfall", "Snowfall", "Relative Humidity (2m)",
            "Visibility", "UV Index", "Chance of Rain", "Weather Condition",
            "Vapour Pressure Deficit"
        ],
        "Units": [
            "ISO 8601 Datetime", "\u00b0C", "\u00b0C", "\u00b0C",
            "km/h", "Degrees", "%", "hPa",
            "hPa", "mm", "mm", "%",
            "km", "Index", "%", "Text",
            "kPa"
        ]
    }

    show = pd.DataFrame(data).set_index("Original Columns")

    Current, Forecast, Weekly_Analysis = st.tabs(['Current', 'Forecast', 'Weekly-Analysis'])

    # --- Weekly Analysis Tab ---
    with Weekly_Analysis:
        st.title("WEEKLY ANALYSIS")
        st.divider()

        df['datetime'] = pd.to_datetime(df['datetime'])
        last_row = df.iloc[-1]

        weather_columns = [col for col in last_row.index if col.startswith("weather")]
        no_show_colmns = [col for col in last_row.index if col.endswith('h')]
        other_columns = ['wind_degrees', 'hour_sin', 'hour_cos', 'wind_x', 'wind_y']
        non_weather_columns = weather_columns + no_show_colmns + other_columns
        df_droped = df.drop(columns=non_weather_columns, errors="ignore")

        st.title("Plotting and Column Details")
        columns_to_plot = [col for col in df_droped.columns if col != "datetime"]
        selected_column = st.selectbox("Select a column to plot:", columns_to_plot)

        if selected_column:
            st.write(f"Plotting datetime against **{selected_column}**")
            st.line_chart(data=df_droped.set_index('datetime')[selected_column])

        st.write("Details of Other Columns:")
        for col in df.columns:
            if col not in non_weather_columns and pd.api.types.is_numeric_dtype(df[col]):
                value = np.mean(df[col])
                user_friendly_name = show.loc[col, 'User-Friendly Names'] if col in show.index else col
                unit_aaociated = show.loc[col, 'Units'] if col in show.index else ""

                st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px; background-color: #808080;">
                        <h4 style="margin: 0;">{user_friendly_name}</h4>
                        <p style="margin: 0;">Mean Value: <strong>{value:.2f} {unit_aaociated}</strong></p>
                    </div>
                """, unsafe_allow_html=True)

    # --- Forecast Tab ---
    with Forecast:
        df_forecast_weather = df.iloc[-1]
        weather_columns = [col for col in df_forecast_weather.index if col.startswith("weather")]
        no_show_colmns = [col for col in df_forecast_weather.index if col.endswith('h')]
        other_columns = ['wind_degrees', 'hour_sin', 'hour_cos', 'wind_x', 'wind_y']
        non_weather_columns = weather_columns + no_show_colmns + other_columns
        df_forecast = df_forecast_weather.drop(non_weather_columns)

        st.header("Hourly Forecast:")

        def display_hourly_cards(base_col, label):
            st.subheader(label)
            with st.container(border=True):
                pred_cols = st.columns(5)
                for i, col in enumerate(pred_cols, 1):
                    with col:
                        st.subheader(df_forecast_weather['datetime'] + timedelta(hours=i))
                        st.divider()
                        st.subheader(f"{df_forecast_weather[f'{base_col}_{i}h'].round(1)}")

        display_hourly_cards("temperature_2m", "Temperature 🌤️")
        st.write("Water vapor is in the air compared to the maximum amount of water vapor the air can hold at a specific temperature.")
        display_hourly_cards("relative_humidity_2m", "Relative Humidity ☁️")
        display_hourly_cards("chance_of_rain", "Chance of Rain 🌧️")

    # --- Current Tab ---
    with Current:
        df_forecast_weather = df.iloc[-1]
        non_weather_columns = [col for col in df_forecast_weather.index if col.startswith("weather") or col.endswith("h")] + ['wind_degrees', 'hour_sin', 'hour_cos', 'wind_x', 'wind_y']
        df_forecast = df_forecast_weather.drop(non_weather_columns)
        row_data = df_forecast

        st.title("Grid Display for Weather Forecast")
        columns_per_row = 4
        keys = [
            f"{show.loc[col, 'User-Friendly Names']} ({show.loc[col, 'Units']})" if col in show.index else col
            for col in row_data.index
        ]
        values = list(row_data.values)

        for i in range(0, len(keys), columns_per_row):
            cols = st.columns(columns_per_row)
            for j, col in enumerate(cols):
                if i + j < len(keys):
                    key = keys[i + j]
                    value = values[i + j]
                    background_color = "#f9f9f9" if (i // columns_per_row) % 2 == 0 else "#e8e8e8"
                    with col:
                        st.markdown(
                            f"""
                            <div style='border-radius: 10px; padding: 10px; margin: 5px; background-color: {background_color}; text-align: center;'>
                                <h4 style='margin: 0; color: #333;'>{key}</h4>
                                <p style='font-size: 20px; margin: 5px 0; color: #555;'><strong>{value}</strong></p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
