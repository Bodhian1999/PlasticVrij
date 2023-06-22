# general_dashboard.py
import streamlit as st
from streamlit_folium import st_folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import folium
import plotly.io as pio

from utils import get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage, calculate_sustainability_score


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
        for _, row in recent_form_responses_df.sort_values('created_at').iterrows():
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


df = pd.DataFrame({'postal_code': ['1102 TS', '1057 AS', '1016 AA', '1016AD']})
df['score'] = [9,6,3,7]
df['name'] = ['Pannenkoekenhuis','Thuis','UvA','Test']

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

# Create an empty list
data_list = []

# Process each data point and add to the list
for _, row in df.iterrows():
    postal_code = row['postal_code']
    coordinates = address_to_coordinates(postal_code)

    if coordinates is not None:
        latitude, longitude = coordinates
        data_list.append({'postal_code': postal_code, 'latitude': latitude, 'longitude': longitude})
    else:
        data_list.append({'postal_code': postal_code, 'latitude': None, 'longitude': None})

# Create a DataFrame from the list
coordinates_df = pd.DataFrame(data_list)

# Merge the original DataFrame with the coordinates DataFrame
df = pd.merge(df, coordinates_df, on='postal_code', how='left')

# Sample data with scores and coordinates
data = df

# Define a function to determine the color based on the score
def get_color(score):
    if score >= (2/3)*10:
        return 'green'  
    elif score >= (1/3)*10:
        return 'orange'  
    else:
        return 'red'  

# Create a Folium map centered on Amsterdam
m = folium.Map(location=[52.377956, 4.897070], zoom_start=12)

# Add markers to the map
for index, row in data.iterrows():
    name = row['name']
    score = row['score']
    latitude = row['latitude']
    longitude = row['longitude']
    color = get_color(score)
    
    # Create the Folium icon with the desired color and icon prefix
    icon = folium.Icon(color=color, icon='map-pin', prefix='fa')
    
    # Define the style for the score text
    score_style = f'color: {color}; font-weight: bold; white-space: nowrap;'
    
    # Create the Folium marker and add it to the map
    folium.Marker(
        location=[latitude, longitude],
        popup=f'<b>{name}</b><br><span style="{score_style}">Score: {score}</span>',
        icon=icon
    ).add_to(m)

# Display the map

    st.markdown('**Kaart**')
    folium_static(m)
    
    # Example: Display general data
    st.write("General data goes here")
    

