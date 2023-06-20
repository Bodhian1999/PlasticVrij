import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from utils import calculate_non_plastics_percentage, get_user_score, get_recent_form_response, get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage

def personal_dashboard_page(current_user_email):

    st.header("Persoonlijk Dashboard")
    st.write(f"Huidige gebruiker: {current_user_email}")

    form_responses_df = get_all_form_responses(current_user_email)
    
    recent_form_responses_df = get_recent_form_responses()
    
    if recent_form_responses_df is not None:
        st.dataframe(recent_form_responses_df)
        avg_sustainability_percentage = calculate_avg_sustainability_percentage(recent_form_responses_df)
        st.write(f"Average Sustainability Percentage: {avg_sustainability_percentage:.2f}%")
    else:
        st.write("No recent form responses found.")
    
    if form_responses_df is not None:
        st.dataframe(form_responses_df)
        
        # Get unique values from the 'created_at' column
        created_at_values = form_responses_df['created_at'].unique()

        # Select the row based on the user's choice of 'created_at'
        selected_created_at = st.selectbox('Selecteer een datum:', created_at_values)

        # Filter the DataFrame to get the selected row
        selected_row = form_responses_df[form_responses_df['created_at'] == selected_created_at]

        # Initialize the counts
        ja_count = 0
        nee_count = 0

        # Loop over the columns between index 3 and 22
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
            title='Totaal Aantal Ja vs Nee voor Alle Categorieën (Geselecteerde Rij)',
            xaxis_title='Antwoord',
            yaxis_title='Aantal',
            showlegend=False
        )
        
        # Display the chart
        st.plotly_chart(fig)
        
        # Initialize the counts
        multi_use_non_plastics_count = 0
        single_use_non_plastics_count = 0
        multi_use_plastics_count = 0
        single_use_plastics_count = 0
        not_applicable_count = 0

        # Loop over the columns between index 22 and 40
        for column in selected_row.columns[22:41]:
            value = selected_row[column].values[0]
            if value == "Multi-Use Non-Plastics":
                multi_use_non_plastics_count += 1
            elif value == "Single-Use Non-Plastics":
                single_use_non_plastics_count += 1
            elif value == "Multi-Use plastics":
                multi_use_plastics_count += 1
            elif value == "Single-Use Plastics":
                single_use_plastics_count += 1
            elif value == "n.v.t. (product uit assortiment gehaald)":
                not_applicable_count += 1

        # Create a bar chart using Plotly
        fig = go.Figure(data=[
            go.Bar(
                x=[
                    "Multi-Use Non-Plastics",
                    "Single-Use Non-Plastics",
                    "Multi-Use plastics",
                    "Single-Use Plastics",
                    "n.v.t. (product uit assortiment gehaald)"
                ],
                y=[
                    multi_use_non_plastics_count,
                    single_use_non_plastics_count,
                    multi_use_plastics_count,
                    single_use_plastics_count,
                    not_applicable_count
                ],
                marker_color=['green', 'blue', 'orange', 'red', 'gray']
            )
        ])

        # Customize the layout
        fig.update_layout(
            title='Aantal Categorieën voor Geselecteerde Rij',
            xaxis_title='Categorie',
            yaxis_title='Aantal',
            showlegend=False
        )

        # Display the chart
        st.plotly_chart(fig)
        
        # Calculate the sustainability percentage
        sustainability_percentage = calculate_sustainability_percentage(selected_row.iloc[:, 22:42]..dropna())

        # Create a pie chart using Plotly
        fig = go.Figure(data=[
            go.Pie(
                labels=['Duurzaam', 'Niet Duurzaam'],
                values=[sustainability_percentage, 100 - sustainability_percentage],
                marker_colors=['green', 'red']
            )
        ])

        # Customize the layout
        fig.update_layout(
            title='Percentage Duurzame Opties',
            showlegend=True
        )

        # Display the chart
        st.plotly_chart(fig)

        st.write("Kolomnamen en Indices:")
        for i, col in enumerate(form_responses_df.columns):
            st.write(f"Index: {i}, Kolom: {col}")
    else:
        st.write("Geen formulierreacties gevonden.")
