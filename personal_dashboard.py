import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from utils import calculate_non_plastics_percentage, get_user_score, get_recent_form_response, get_all_form_responses

def personal_dashboard_page(current_user_email):

    st.header("Persoonlijk Dashboard")
    st.write(f"Huidige gebruiker: {current_user_email}")

    form_responses_df = get_all_form_responses(current_user_email)
    
    if form_responses_df is not None:
        st.dataframe(form_responses_df)
        
        # Get unique values from the 'created_at' column
        created_at_values = form_responses_df['created_at'].unique()

        # Select the row based on the user's choice of 'created_at'
        selected_created_at = st.selectbox('Select a date:', created_at_values)

        # Filter the DataFrame to get the selected row
        selected_row = form_responses_df[form_responses_df['created_at'] == selected_created_at]

        # Initialize the counts
        ja_count = 0
        nee_count = 0

        # Loop over the columns between i
        for column in selected_row.columns[3:22]:
            if selected_row[column].values[0] == 'Ja':
                ja_count += 1
            elif selected_row[column].values[0] == 'Nee':
                nee_count += 1

        # Create a bar chart using Plotly
        fig = go.Figure(data=[
            go.Bar(x=['Ja', 'Nee'], y=[ja_count, nee_count], marker_color=['green', 'red'])
        ])

        # Customize the layout
        fig.update_layout(
            title='Total Count of Ja vs Nee for All Categories (Selected Row)',
            xaxis_title='Answer',
            yaxis_title='Count',
            showlegend=False
        )
        
        # Display the chart
        st.plotly_chart(fig)
        
        st.write("Column Names and Indices:")
        for i, col in enumerate(form_responses_df.columns):
            st.write(f"Index: {i}, Column: {col}")
    else:
        st.write("No form responses found.")
        
        

