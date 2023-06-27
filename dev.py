import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
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
            'Product Category': categories,
            'Cost Savings (%)': np.random.uniform(5, 30, len(categories))
        })

        # Generate sample data for environmental impact comparison
        metrics = ['Carbon Footprint', 'Water Usage', 'Waste Generation']

        sample_data['Carbon Footprint'] = np.random.uniform(100, 1000, len(categories))
        sample_data['Water Usage'] = np.random.uniform(1000, 10000, len(categories))
        sample_data['Waste Generation'] = np.random.uniform(10, 100, len(categories))

        # Normalize the environmental impact metrics to percentages
        for metric in metrics:
            sample_data[metric] = (sample_data[metric] - sample_data[metric].min()) / (
                sample_data[metric].max() - sample_data[metric].min()
            ) * 100

        # Create the cost savings comparison bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(sample_data['Product Category'], sample_data['Cost Savings (%)'])
        plt.xlabel('Product Category')
        plt.ylabel('Cost Savings (%)')
        plt.title('Comparison of Cost Savings: Plastic vs. Sustainable Alternatives')
        plt.xticks(rotation=90)
        plt.tight_layout()
        st.pyplot()  # Display the plot using Streamlit's `st.pyplot` function

        # Create the environmental impact comparison stacked bar chart
        fig = go.Figure()
        fig.add_trace(go.Bar(x=sample_data['Product Category'], y=sample_data['Carbon Footprint'], name='Carbon Footprint'))
        fig.add_trace(go.Bar(x=sample_data['Product Category'], y=sample_data['Water Usage'], name='Water Usage', 
                             bottom=sample_data['Carbon Footprint']))
        fig.add_trace(go.Bar(x=sample_data['Product Category'], y=sample_data['Waste Generation'], name='Waste Generation', 
                             bottom=sample_data['Carbon Footprint'] + sample_data['Water Usage']))
        fig.update_layout(barmode='stack', xaxis_tickangle=-90,
                          title='Environmental Impact Comparison: Plastic vs. Sustainable Materials',
                          xaxis=dict(title='Product Category'),
                          yaxis=dict(title='Environmental Impact (%)'))
        st.plotly_chart(fig)  # Display the plotly chart using Streamlit's `st.plotly_chart` function
        
    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
