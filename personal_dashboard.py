import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from utils import get_recent_form_response, get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage, calculate_sustainability_score

def personal_dashboard_page(current_user_email):

    st.header("Jouw Dashboard")
    st.write(f"Huidige gebruiker: {current_user_email}")

    form_responses_df = get_all_form_responses(current_user_email)
    sustainability_percentages = form_responses_df.apply(calculate_sustainability_percentage, axis=1)

    if form_responses_df is not None:
        st.write("Hieronder vindt je de door jou ingezonden formulierreacties.")
        st.dataframe(form_responses_df)
        
        # Get unique values from the 'created_at' column
        created_at_values = form_responses_df['created_at'].unique()

        # Select the row based on the user's choice of 'created_at'
        selected_created_at = st.selectbox('Selecteer welk formulier je voor het dashboard wil gebruiken:', created_at_values)

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
        
        st.subheader("Totaal Aantal gebruikt vs weggelaten voor Alle Categorieën")
        st.write("Hieronder wordt weergegeven hoeveel van de categorieën die we behandelen door jou worden gebruikt.")

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

        st.subheader("Verdeling van opties voor verpakking")
        st.write("Hieronder wordt het aantal reacties per optie weergegeven.")

        # Display the chart
        st.plotly_chart(fig)
        
        # Create a line chart to visualize the sustainability percentages over time
        fig = go.Figure(data=[
            go.Scatter(x=form_responses_df['created_at'], y=sustainability_percentages, mode='lines+markers')
        ])
        fig.update_layout(
            title='Duurzaamheidspercentage over tijd',
            xaxis_title='Datum',
            yaxis_title='Duurzaamheidspercentage'
        )
        st.subheader("Duurzaamheidspercentage over tijd")
        st.plotly_chart(fig)

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
