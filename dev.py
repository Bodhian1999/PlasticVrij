import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import get_recent_form_response, get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage, calculate_sustainability_score

def dev(current_user_email):
    st.header("Overzicht van jouw Duurzaamheidsinspanningen")
    st.write(f"Huidige gebruiker: {current_user_email}")

    form_responses_df = get_all_form_responses(current_user_email)

    recent_form_responses_df = get_recent_form_responses()

    if form_responses_df is not None:
        st.write("---")
        st.subheader("Ingezonden formulierreacties")
        st.write("Hieronder vindt je de door jou ingezonden formulierreacties.")

        # Generate sample data for cost savings comparison
        years = np.arange(1, 11)  # Years 1 to 10

        # Calculate the cost of multi-use non-plastic straws
        multi_use_non_plastic_cost = np.full(len(years), 100)  # Cost of 200 reusable non-plastic straws
        replace_interval_multi_use_non_plastic = 5  # Number of years before replacement
        replacement_cost_multi_use_non_plastic = 100  # Cost of replacement
        for i in range(replace_interval_multi_use_non_plastic, len(years), replace_interval_multi_use_non_plastic):
            multi_use_non_plastic_cost[i:] += replacement_cost_multi_use_non_plastic

        # Calculate the cost of multi-use plastic straws
        multi_use_plastic_cost = np.full(len(years), 60)  # Cost of 200 reusable plastic straws
        replace_interval_multi_use_plastic = 2  # Number of years before replacement
        replacement_cost_multi_use_plastic = 60  # Cost of replacement
        for i in range(replace_interval_multi_use_plastic, len(years), replace_interval_multi_use_plastic):
            multi_use_plastic_cost[i:] += replacement_cost_multi_use_plastic

        # Calculate the cost of single-use non-plastic straws
        single_use_non_plastic_cost = np.full(len(years), 60)  # Cost of 1000 single-use non-plastic straws
        replace_interval_single_use_non_plastic = 1  # Number of years before replacement
        replacement_cost_single_use_non_plastic = 60  # Cost of replacement
        for i in range(replace_interval_single_use_non_plastic, len(years), replace_interval_single_use_non_plastic):
            single_use_non_plastic_cost[i:] += replacement_cost_single_use_non_plastic

        # Calculate the cost of single-use plastic straws
        single_use_plastic_cost = np.full(len(years), 20)  # Cost of 1000 single-use plastic straws
        replace_interval_single_use_plastic = 1  # Number of years before replacement
        replacement_cost_single_use_plastic = 20  # Cost of replacement
        for i in range(replace_interval_single_use_plastic, len(years), replace_interval_single_use_plastic):
            single_use_plastic_cost[i:] += replacement_cost_single_use_plastic

        # Create the cost savings comparison line plot
        data = pd.DataFrame({
            'Years': years,
            'Multi-Use Non-Plastic': multi_use_non_plastic_cost,
            'Multi-Use Plastic': multi_use_plastic_cost,
            'Single-Use Non-Plastic': single_use_non_plastic_cost,
            'Single-Use Plastic': single_use_plastic_cost
        })

        selected_data = data[['Years', 'Multi-Use Non-Plastic', 'Multi-Use Plastic', 'Single-Use Non-Plastic', 'Single-Use Plastic']]

        fig = px.line(selected_data, x='Years', y=['Multi-Use Non-Plastic', 'Multi-Use Plastic', 'Single-Use Non-Plastic', 'Single-Use Plastic'], 
                      title='Cost Savings Comparison: Straws - Plastic vs. Sustainable Alternatives')
        fig.update_layout(xaxis_title='Years', yaxis_title='Cost ($)')
        st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
