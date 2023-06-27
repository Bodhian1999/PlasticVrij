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
        categories = [
            'rietjes', 'honingstaafjes', 'melkcupjes', 'suikerzakjes', 'koekjeswrappers',
            'theezakjes_verpakking', 'ontbijt_boter', 'ontbijt_jam_pindakaas_chocoladepasta',
            'saus_mayonaise', 'saus_ketchup', 'saus_mosterd', 'saus_soya_saus',
            'pepermuntverpakking', 'snoepjes_rekening', 'tandenstokerverpakking',
            'stampers', 'wegwerpbekers_feesten_partijen', 'ijsjes_plastic_verpakking',
            'natte_doekjes_garnalen_spareribs'
        ]

        st.write(categories)

        sample_data = pd.DataFrame({
            'Category': categories,
            'Multi-Use Non-Plastics': np.random.uniform(50, 150, len(categories)),
            'Single-Use Non-Plastics': np.random.uniform(30, 100, len(categories)),
            'Multi-Use Plastics': np.random.uniform(20, 80, len(categories)),
            'Single-Use Plastics': np.random.uniform(10, 60, len(categories))
        })

        # Create the cost savings comparison line plot
        fig = px.line(sample_data, x='Category', y=['Multi-Use Non-Plastics', 'Single-Use Non-Plastics', 'Multi-Use Plastics', 'Single-Use Plastics'], title='Cost Savings Comparison: Plastic vs. Sustainable Alternatives')
        fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': categories}, xaxis_title='Category', yaxis_title='Cost')
        st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function

    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
