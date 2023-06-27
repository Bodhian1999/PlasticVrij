import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def dev(current_user_email):
    st.header("Overzicht van jouw Duurzaamheidsinspanningen")
    st.write(f"Huidige gebruiker: {current_user_email}")

    form_responses_df = get_all_form_responses(current_user_email)

    recent_form_responses_df = get_recent_form_responses()

    if form_responses_df is not None:
        st.write("---")
        st.subheader("Ingezonden formulierreacties")
        st.write("Hieronder vindt je de door jou ingezonden formulierreacties.")

        # Generate sample data for cost comparison
        years = np.arange(1, 11)  # Years 1 to 10
        single_use_plastic_cost = np.full(len(years), 1000)  # Cost of single-use plastics per year
        multi_use_non_plastic_investment = 3000  # Initial investment for multi-use non-plastics
        multi_use_non_plastic_cost = np.full(len(years), multi_use_non_plastic_investment)  # Cost of multi-use non-plastics

        # Increase the cost of multi-use non-plastics every 5 years
        replace_interval = 5  # Number of years before replacement
        replacement_cost = 3000  # Cost of replacement
        for i in range(replace_interval, len(years), replace_interval):
            multi_use_non_plastic_cost[i:] += replacement_cost

        # Create the cost savings comparison line plot
        data = pd.DataFrame({
            'Years': years,
            'Single-Use Plastics': np.cumsum(single_use_plastic_cost),
            'Multi-Use Non-Plastics': multi_use_non_plastic_cost
        })

        selected_data = data[['Years', 'Single-Use Plastics', 'Multi-Use Non-Plastics']]

        fig = px.line(selected_data, x='Years', y=['Single-Use Plastics', 'Multi-Use Non-Plastics'], title='Cost Savings Comparison: Plastic vs. Sustainable Alternatives')
        fig.update_layout(xaxis_title='Years', yaxis_title='Cost (€)')
        st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
