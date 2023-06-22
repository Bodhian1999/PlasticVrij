# general_dashboard.py
import streamlit as st
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import numpy as np
import plotly.graph_objects as go
from utils import get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage, calculate_sustainability_score

import folium

def general_dashboard_page(current_user_email):
    st.header("General Dashboard")
    
    st.write(f"Huidige gebruiker: {current_user_email}")
    recent_form_responses_df = get_recent_form_responses()

    if recent_form_responses_df is not None:
        # Create a new column to store the sustainability percentages
        recent_form_responses_df['Sustainability Percentage'] = None

        # Calculate average sustainability percentage
        recent_form_responses_df['avg_sustainability_percentage'] = calculate_avg_sustainability_percentage(recent_form_responses_df)

        # Create a new DataFrame for tracking average sustainability scores over time
        avg_sus_score_df = pd.DataFrame(columns=['Date', 'Average Sustainability Score'])
        prev_avg_sustainability_percentage = None

       # Iterate over the rows and calculate the sustainability percentage
        for _, row in recent_form_responses_df.iterrows():
            row_df = pd.DataFrame(row).transpose()  # Convert the Series to DataFrame
            sustainability_percentage = calculate_sustainability_percentage(row_df[row_df.columns[22:41]])
            recent_form_responses_df.at[_, 'Sustainability Percentage'] = sustainability_percentage
            
            if sustainability_percentage is not None and prev_avg_sustainability_percentage is not None:
                if sustainability_percentage != prev_avg_sustainability_percentage:
                    new_row = pd.DataFrame({'Date': [row['created_at']], 'Average Sustainability Score': [sustainability_percentage]})
                    avg_sus_score_df = pd.concat([avg_sus_score_df, new_row], ignore_index=True)
                    prev_avg_sustainability_percentage = sustainability_percentage
            else:
                new_row = pd.DataFrame({'Date': [row['created_at']], 'Average Sustainability Score': [sustainability_percentage]})
                avg_sus_score_df = pd.concat([avg_sus_score_df, new_row], ignore_index=True)
                prev_avg_sustainability_percentage = sustainability_percentage
        
        st.dataframe(recent_form_responses_df)
        
        # Create a line chart to visualize the sustainability percentages over time
        fig = go.Figure(data=[
            go.Scatter(x=avg_sus_score_df['Date'], y=avg_sus_score_df['Average Sustainability Score'], mode='lines+markers')
        ])
        fig.update_layout(
            xaxis_title='Datum',
            yaxis_title='Duurzaamheidspercentage'
        )
        st.subheader("Duurzaamheidspercentage over tijd")
        st.plotly_chart(fig)
    else:
        st.write("Er zijn geen ingevulde formulieren gevonden")
    
    def address_to_coordinates(postal_code):
        address = f"{postal_code}, Netherlands"
        geolocator = Nominatim(user_agent="my_geocoder")

        try:
            location = geolocator.geocode(address, exactly_one=True, country_codes="NL", timeout=10)
        except GeocoderTimedOut:
            return address_to_coordinates(postal_code)  # Retry on timeout

        if location is None:
            return None

        latitude = location.latitude
        longitude = location.longitude
        return latitude, longitude

    data = pd.DataFrame({'postal_code': ['1102 TS', '1057 AS', '1016 AA']})

    data_list = []

    for _, row in data.iterrows():
        postal_code = row['postal_code']
        coordinates = address_to_coordinates(postal_code)

        if coordinates is not None:
            latitude, longitude = coordinates
            data_list.append({'postal_code': postal_code, 'latitude': latitude, 'longitude': longitude})
        else:
            data_list.append({'postal_code': postal_code, 'latitude': None, 'longitude': None})

    df = pd.DataFrame(data_list)

    m = folium.Map(location=[52.377956, 4.897070], zoom_start=11)

    pin_icon = folium.Icon(icon='glyphicon glyphicon-pushpin', prefix='glyphicon')

    for index, row in df.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        postal_code = row['postal_code']
        label = f"Postal Code: {postal_code}"
        folium.Marker(location=[lat, lon], tooltip=label, icon=folium.Icon(color='red', icon='map-pin', prefix='fa')).add_to(m)

    st.markdown('**Kaart**')
    folium_static(m)
    
    # Example: Display general data
    st.write("General data goes here")
    

