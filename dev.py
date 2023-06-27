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

        # Average costs per year for each category
        multi_use_non_plastics_cost = [100, 50, 70, 60, 80, 70, 80, 90, 100, 90, 70, 80, 60, 100, 110, 70, 80, 90, 70]
        single_use_non_plastics_cost = [60, 40, 50, 40, 30, 40, 50, 50, 60, 50, 40, 50, 30, 70, 80, 40, 50, 60, 40]
        multi_use_plastics_cost = [60, 30, 40, 50, 30, 40, 50, 60, 70, 60, 50, 40, 30, 80, 90, 50, 40, 50, 30]
        single_use_plastics_cost = [20, 10, 15, 20, 10, 15, 20, 20, 30, 20, 15, 10, 10, 40, 50, 10, 15, 20, 10]

        # Replacement intervals for reusable options
        multi_use_non_plastics_replace_interval = 5  # Replace every 5 years
        multi_use_plastics_replace_interval = 3  # Replace every 3 years

        selected_category = st.selectbox("Select Category", categories)

        # Get the cost and replacement interval for the selected category
        if selected_category in categories:
            category_index = categories.index(selected_category)
            cost_multi_use_non_plastics = multi_use_non_plastics_cost[category_index]
            cost_single_use_non_plastics = single_use_non_plastics_cost[category_index]
            cost_multi_use_plastics = multi_use_plastics_cost[category_index]
            cost_single_use_plastics = single_use_plastics_cost[category_index]
            replace_interval_multi_use_non_plastics = multi_use_non_plastics_replace_interval
            replace_interval_multi_use_plastics = multi_use_plastics_replace_interval

            # Generate sample data for cost comparison
            years = np.arange(1, 11)  # Years 1 to 10

            # Cost of single-use plastics per year
            single_use_plastic_cost = np.full(len(years), cost_single_use_plastics)
            
            # Cost of reusable options per year
            multi_use_non_plastic_cost = np.full(len(years), cost_multi_use_non_plastics)
            multi_use_plastic_cost = np.full(len(years), cost_multi_use_plastics)
            single_use_non_plastic_cost = np.full(len(years), cost_single_use_non_plastics)

            # Increase the cost of reusable options every replacement interval
            for i in range(0, len(years)):
                if (i + 1) % replace_interval_multi_use_non_plastics == 0:
                    multi_use_non_plastic_cost[i] += cost_multi_use_non_plastics
                if (i + 1) % replace_interval_multi_use_plastics == 0:
                    multi_use_plastic_cost[i] += cost_multi_use_plastics

            # Create the cost savings comparison line plot
            data = pd.DataFrame({
                'Years': years,
                'Single-Use Plastics': np.cumsum(single_use_plastic_cost),
                'Multi-Use Non-Plastics': np.cumsum(multi_use_non_plastic_cost),
                'Multi-Use Plastics': np.cumsum(multi_use_plastic_cost),
                'Single-Use Non-Plastics': np.cumsum(single_use_non_plastic_cost)
            })

            selected_data = data[['Years', 'Single-Use Plastics', 'Multi-Use Non-Plastics', 'Multi-Use Plastics', 'Single-Use Non-Plastics']]

            fig = px.line(selected_data, x='Years', y=['Single-Use Plastics', 'Multi-Use Non-Plastics', 'Multi-Use Plastics', 'Single-Use Non-Plastics'],
                          title='Cost Comparison: Plastic vs. Sustainable Alternatives - Category: {}'.format(selected_category))
            fig.update_layout(xaxis_title='Years', yaxis_title='Cost ($)')
            st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
