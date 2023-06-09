import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from utils import get_recent_form_response, get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage, calculate_sustainability_score

def personal_dashboard_page(current_user_email):
    st.header("Overzicht van jouw Duurzaamheidsinspanningen")
    st.write(f"Huidige gebruiker: {current_user_email}")

    form_responses_df = get_all_form_responses(current_user_email)
    
    recent_form_responses_df = get_recent_form_responses()
    
    
    if form_responses_df is not None:
        st.write("---")
        st.subheader("Ingezonden formulierreacties") 
        st.write("Hieronder vindt je de door jou ingezonden formulierreacties.")
        
        # Create a new column to store the sustainability percentages
        form_responses_df['Sustainability Percentage'] = None
        
        # Iterate over the rows and calculate the sustainability percentage and user score
        for _, row in form_responses_df.iterrows():
            row_df = pd.DataFrame(row).transpose()  # Convert the Series to DataFrame
            sustainability_percentage = calculate_sustainability_percentage(row_df[row_df.columns[22:41]])
            form_responses_df.at[_, 'Sustainability Percentage'] = sustainability_percentage
        
        st.dataframe(form_responses_df)
        
        
        # Get unique values from the 'created_at' column
        created_at_values = form_responses_df['created_at'].unique()

        # Select the row based on the user's choice of 'created_at'
        st.write("---")
        st.subheader("Formulierreactieselectie")
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
            xaxis_title='Antwoord',
            yaxis_title='Aantal',
            showlegend=False
        )
        
        # Totaal Aantal gebruikt vs weggelaten voor Alle Categorieën
        st.write("---")
        st.subheader("Totaal Aantal gebruikt vs weggelaten voor Alle Categorieën")
        st.write("Hieronder zie je hoeveel categorieën je momenteel gebruikt en welke je nog kunt verbeteren. Laten we samen kijken naar jouw duurzaamheidsprofiel.")

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
            xaxis_title='Categorie',
            yaxis_title='Aantal',
            showlegend=False
        )

        # Verdeling van opties voor verpakking
        st.write("---")
        st.subheader("Verdeling van opties voor verpakking")
        st.write("Deze grafiek toont de verdeling van de verpakkingsopties die je momenteel kiest. Het helpt om de meest gebruikte verpakkingstypes te identificeren en te focussen op duurzamere alternatieven.")


        # Display the chart
        st.plotly_chart(fig)
        
        # Calculate the sustainability percentage
        sustainability_percentage = calculate_sustainability_percentage(selected_row[selected_row.columns[22:41]])

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
            showlegend=True
        )

       # Percentage Duurzame Opties
        st.write("---")
        st.subheader("Percentage Duurzame Opties")
        st.write("Hier zie je het percentage duurzame opties dat je al hebt gekozen. Een hoger percentage betekent een grotere bijdrage aan een duurzamere wereld.")

        # Display the chart
        st.plotly_chart(fig)
             
        # Calculate average sustainability percentage
        avg_sustainability_percentage = calculate_avg_sustainability_percentage(recent_form_responses_df)
        
        # Create the bar chart
        fig = go.Figure(data=[
            go.Bar(name='Gebruiker', x=['Gebruiker'], y=[sustainability_percentage]),
            go.Bar(name='Gemiddelde', x=['Gemiddelde'], y=[avg_sustainability_percentage])
        ])

        # Customize the layout
        fig.update_layout(xaxis_title='Categorie',
                          yaxis_title='Percentage',
                          barmode='group')

        # Vergelijking Duurzaamheidspercentage
        st.write("---")
        st.subheader("Vergelijking Duurzaamheidspercentage")
        st.write("We vergelijken jouw duurzaamheidspercentage met het gemiddelde percentage van andere gebruikers. Dit geeft je inzicht in jouw vooruitgang.")

        # Display the chart
        st.plotly_chart(fig)
        
        # Create a line chart to visualize the sustainability percentages over time
        fig = go.Figure(data=[
            go.Scatter(x=form_responses_df['created_at'], y=form_responses_df['Sustainability Percentage'], mode='lines+markers')
        ])
        fig.update_layout(
            xaxis_title='Datum',
            yaxis_title='Duurzaamheidspercentage'
        )
        
        # Duurzaamheidspercentage over tijd
        st.write("---")
        st.subheader("Duurzaamheidspercentage over tijd")
        st.write("Deze lijngrafiek laat zien hoe jouw duurzaamheidspercentage zich in de loop van de tijd heeft ontwikkeld.")
             
        st.plotly_chart(fig)
        
    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
