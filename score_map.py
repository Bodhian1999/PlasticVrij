import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from utils import calculate_non_plastics_percentage, get_recent_form_response, get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage, calculate_sustainability_score

recent_form_responses_df = get_recent_form_responses()
# Calculate average sustainability percentage
avg_sustainability_percentage = calculate_avg_sustainability_percentage(recent_form_responses_df)

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