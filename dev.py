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

        # Calculate the cost of straws
        multi_use_non_plastic_straws_cost = np.full(len(years), 100)  # Cost of 200 reusable non-plastic straws
        replace_interval_multi_use_non_plastic_straws = 5  # Number of years before replacement
        replacement_cost_multi_use_non_plastic_straws = 100  # Cost of replacement
        for i in range(replace_interval_multi_use_non_plastic_straws, len(years), replace_interval_multi_use_non_plastic_straws):
            multi_use_non_plastic_straws_cost[i:] += replacement_cost_multi_use_non_plastic_straws

        multi_use_plastic_straws_cost = np.full(len(years), 60)  # Cost of 200 reusable plastic straws
        replace_interval_multi_use_plastic_straws = 2  # Number of years before replacement
        replacement_cost_multi_use_plastic_straws = 60  # Cost of replacement
        for i in range(replace_interval_multi_use_plastic_straws, len(years), replace_interval_multi_use_plastic_straws):
            multi_use_plastic_straws_cost[i:] += replacement_cost_multi_use_plastic_straws

        single_use_non_plastic_straws_cost = np.full(len(years), 60)  # Cost of 1000 single-use non-plastic straws
        replace_interval_single_use_non_plastic_straws = 1  # Number of years before replacement
        replacement_cost_single_use_non_plastic_straws = 60  # Cost of replacement
        for i in range(replace_interval_single_use_non_plastic_straws, len(years), replace_interval_single_use_non_plastic_straws):
            single_use_non_plastic_straws_cost[i:] += replacement_cost_single_use_non_plastic_straws

        single_use_plastic_straws_cost = np.full(len(years), 20)  # Cost of 1000 single-use plastic straws
        replace_interval_single_use_plastic_straws = 1  # Number of years before replacement
        replacement_cost_single_use_plastic_straws = 20  # Cost of replacement
        for i in range(replace_interval_single_use_plastic_straws, len(years), replace_interval_single_use_plastic_straws):
            single_use_plastic_straws_cost[i:] += replacement_cost_single_use_plastic_straws

        # Calculate the cost of honey
        multi_use_non_plastic_honey_cost = np.full(len(years), 300)  # Cost of packaged honey (multi-use non-plastic)
        replace_interval_multi_use_non_plastic_honey = 5  # Number of years before replacement
        replacement_cost_multi_use_non_plastic_honey = 300  # Cost of replacement
        for i in range(replace_interval_multi_use_non_plastic_honey, len(years), replace_interval_multi_use_non_plastic_honey):
            multi_use_non_plastic_honey_cost[i:] += replacement_cost_multi_use_non_plastic_honey

        multi_use_plastic_honey_cost = np.full(len(years), 450)  # Cost of packaged honey (multi-use plastic)
        replace_interval_multi_use_plastic_honey = 2  # Number of years before replacement
        replacement_cost_multi_use_plastic_honey = 450  # Cost of replacement
        for i in range(replace_interval_multi_use_plastic_honey, len(years), replace_interval_multi_use_plastic_honey):
            multi_use_plastic_honey_cost[i:] += replacement_cost_multi_use_plastic_honey

        single_use_non_plastic_honey_cost = np.full(len(years), 210)  # Cost of packaged honey (single-use non-plastic)
        replace_interval_single_use_non_plastic_honey = 1  # Number of years before replacement
        replacement_cost_single_use_non_plastic_honey = 2100  # Cost of replacement
        for i in range(replace_interval_single_use_non_plastic_honey, len(years), replace_interval_single_use_non_plastic_honey):
            single_use_non_plastic_honey_cost[i:] += replacement_cost_single_use_non_plastic_honey

        single_use_plastic_honey_cost = np.full(len(years), 185)  # Cost of packaged honey (single-use plastic)
        replace_interval_single_use_plastic_honey = 1  # Number of years before replacement
        replacement_cost_single_use_plastic_honey = 1850  # Cost of replacement
        for i in range(replace_interval_single_use_plastic_honey, len(years), replace_interval_single_use_plastic_honey):
            single_use_plastic_honey_cost[i:] += replacement_cost_single_use_plastic_honey

        # Create the cost savings comparison line plot
        categories = ['Straws', 'Honey']
        selected_category = st.selectbox("Select Category", categories)

        if selected_category == 'Straws':
            data = pd.DataFrame({
                'Years': years,
                'Multi-Use Non-Plastic Straws': multi_use_non_plastic_straws_cost,
                'Multi-Use Plastic Straws': multi_use_plastic_straws_cost,
                'Single-Use Non-Plastic Straws': single_use_non_plastic_straws_cost,
                'Single-Use Plastic Straws': single_use_plastic_straws_cost
            })
        elif selected_category == 'Honey':
            data = pd.DataFrame({
                'Years': years,
                'Multi-Use Non-Plastic Honey': multi_use_non_plastic_honey_cost,
                'Multi-Use Plastic Honey': multi_use_plastic_honey_cost,
                'Single-Use Non-Plastic Honey': single_use_non_plastic_honey_cost,
                'Single-Use Plastic Honey': single_use_plastic_honey_cost
            })

        selected_data = data[['Years', f'Multi-Use Non-Plastic {selected_category}', f'Multi-Use Plastic {selected_category}', 
                              f'Single-Use Non-Plastic {selected_category}', f'Single-Use Plastic {selected_category}']]

        fig = px.line(selected_data, x='Years', y=[f'Multi-Use Non-Plastic {selected_category}', f'Multi-Use Plastic {selected_category}', 
                                                    f'Single-Use Non-Plastic {selected_category}', f'Single-Use Plastic {selected_category}'], 
                      title=f'Cost Savings Comparison: {selected_category} - Plastic vs. Sustainable Alternatives')
        fig.update_layout(xaxis_title='Years', yaxis_title='Cost ($)')
        st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
