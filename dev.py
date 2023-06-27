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

        # Calculate the cost of reusable straws (steel)
        reusable_steel_straws_cost = np.full(len(years), 100)  # Cost of 200 reusable straws (steel)
        replace_interval_steel = 5  # Number of years before replacement
        replacement_cost_steel = 100  # Cost of replacement
        for i in range(replace_interval_steel, len(years), replace_interval_steel):
            reusable_steel_straws_cost[i:] += replacement_cost_steel

        # Calculate the cost of reusable straws (silicone)
        reusable_silicone_straws_cost = np.full(len(years), 60)  # Cost of 200 reusable straws (silicone)
        replace_interval_silicone = 2  # Number of years before replacement
        replacement_cost_silicone = 60  # Cost of replacement
        for i in range(replace_interval_silicone, len(years), replace_interval_silicone):
            reusable_silicone_straws_cost[i:] += replacement_cost_silicone

        # Calculate the cost of paper straws (single-use non-plastic)
        paper_straws_cost = np.full(len(years), 60)  # Cost of 1000 paper straws
        replace_interval_paper = 1  # Number of years before replacement
        replacement_cost_paper = 60  # Cost of replacement
        for i in range(replace_interval_paper, len(years), replace_interval_paper):
            paper_straws_cost[i:] += replacement_cost_paper

        # Calculate the cost of plastic straws (single-use plastic)
        plastic_straws_cost = np.full(len(years), 20)  # Cost of 1000 plastic straws
        replace_interval_plastic = 1  # Number of years before replacement
        replacement_cost_plastic = 20  # Cost of replacement
        for i in range(replace_interval_plastic, len(years), replace_interval_plastic):
            plastic_straws_cost[i:] += replacement_cost_plastic

        # Create the cost savings comparison line plot
        data = pd.DataFrame({
            'Years': years,
            'Reusable Steel Straws': reusable_steel_straws_cost,
            'Reusable Silicone Straws': reusable_silicone_straws_cost,
            'Paper Straws': paper_straws_cost,
            'Plastic Straws': plastic_straws_cost
        })

        selected_data = data[['Years', 'Reusable Steel Straws', 'Reusable Silicone Straws', 'Paper Straws', 'Plastic Straws']]

        fig = px.line(selected_data, x='Years', y=['Reusable Steel Straws', 'Reusable Silicone Straws', 'Paper Straws', 'Plastic Straws'], 
                      title='Cost Savings Comparison: Straws - Plastic vs. Sustainable Alternatives')
        fig.update_layout(xaxis_title='Years', yaxis_title='Cost ($)')
        st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
