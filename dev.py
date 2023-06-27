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

        categories = [
            'rietjes', 'honingstaafjes', 'melkcupjes', 'suikerzakjes', 'koekjeswrappers',
            'theezakjes_verpakking', 'ontbijt_boter', 'ontbijt_jam_pindakaas_chocoladepasta',
            'saus_mayonaise', 'saus_ketchup', 'saus_mosterd', 'saus_soya_saus',
            'pepermuntverpakking', 'snoepjes_rekening', 'tandenstokerverpakking',
            'stampers', 'wegwerpbekers_feesten_partijen', 'ijsjes_plastic_verpakking',
            'natte_doekjes_garnalen_spareribs'
        ]

        selected_category = st.selectbox("Select Category", categories)

        # Average costs per year for each category
        multi_use_non_plastics_cost = [100, 50, 70, 60, 80, 70, 80, 90, 100, 90, 70, 80, 60, 100, 110, 70, 80, 90, 70]
        single_use_non_plastics_cost = [60, 40, 50, 40, 30, 40, 50, 50, 60, 50, 40, 50, 30, 70, 80, 40, 50, 60, 40]
        multi_use_plastics_cost = [60, 30, 40, 50, 30, 40, 50, 60, 70, 60, 50, 40, 30, 80, 90, 50, 40, 50, 30]
        single_use_plastics_cost = [20, 10, 15, 20, 10, 15, 20, 20, 30, 20, 15, 10, 10, 40, 50, 10, 15, 20, 10]

        # Generate sample data for cost comparison
        years = np.arange(1, 11)  # Years 1 to 10

        # Cost of single-use plastics per year
        single_use_plastic_cost = np.full(len(years), single_use_plastics_cost[categories.index(selected_category)])

        # Cost of reusable options per year
        multi_use_non_plastic_cost = np.full(len(years), multi_use_non_plastics_cost[categories.index(selected_category)])
        multi_use_plastic_cost = np.full(len(years), multi_use_plastics_cost[categories.index(selected_category)])

        # Replacement intervals for reusable options
        multi_use_non_plastics_replace_interval = 5
        multi_use_plastics_replace_interval = 3

        # Increase the cost of reusable options based on the replacement intervals
        for i in range(len(years)):
            if years[i] % multi_use_non_plastics_replace_interval == 0:
                multi_use_non_plastic_cost[i:] += multi_use_non_plastics_cost[categories.index(selected_category)]
            if years[i] % multi_use_plastics_replace_interval == 0:
                multi_use_plastic_cost[i:] += multi_use_plastics_cost[categories.index(selected_category)]

        # Create the cost savings comparison line plot
        data = pd.DataFrame({
            'Years': years,
            'Single-Use Plastics': np.cumsum(single_use_plastic_cost),
            'Multi-Use Non-Plastics': np.cumsum(multi_use_non_plastic_cost),
            'Multi-Use Plastics': np.cumsum(multi_use_plastic_cost),
            'Single-Use Non-Plastics': np.cumsum(single_use_non_plastics_cost)
        })

        selected_data = data[['Years', 'Single-Use Plastics', 'Multi-Use Non-Plastics', 'Multi-Use Plastics', 'Single-Use Non-Plastics']]

        fig = px.line(selected_data, x='Years', y=['Single-Use Plastics', 'Multi-Use Non-Plastics', 'Multi-Use Plastics', 'Single-Use Non-Plastics'], title='Cost Savings Comparison: Plastic vs. Sustainable Alternatives')
        fig.update_layout(xaxis_title='Years', yaxis_title='Cost ($)')
        st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
