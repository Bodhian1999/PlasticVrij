import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import get_recent_form_response, get_all_form_responses, calculate_sustainability_percentage, get_recent_form_responses, calculate_avg_sustainability_percentage, calculate_sustainability_score

def dev(current_user_email):
    st.header("Mogelijkheden bij Voortzetting van het Project")
    st.subheader("Overzicht van Duurzaamheidsinspanningen")
    st.write(f"Doel van deze pagina: Het verkennen van mogelijke duurzaamheidsinspanningen voor verdere ontwikkeling van het project.")
    st.write("---")
    
    st.write("**Disclaimer:**")
    st.write("De gegevens op deze pagina zijn slechts een ruwe schatting en mogen niet als feitelijk worden beschouwd.")
    st.write("---")
    
    st.subheader("Kostenbesparingen Vergelijking: Plastic vs. Duurzame Alternatieven")
    st.write("Deze plot toont een vergelijking van de kostenbesparingen tussen verschillende typen producten. Het stelt je in staat om de mogelijke kostenbesparingen te evalueren bij het gebruik van duurzame alternatieven in vergelijking met plastic producten.")
    
    form_responses_df = get_all_form_responses(current_user_email)

    recent_form_responses_df = get_recent_form_responses()

    if form_responses_df is not None:

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
        replacement_cost_single_use_non_plastic_honey = 210  # Cost of replacement
        for i in range(replace_interval_single_use_non_plastic_honey, len(years), replace_interval_single_use_non_plastic_honey):
            single_use_non_plastic_honey_cost[i:] += replacement_cost_single_use_non_plastic_honey

        single_use_plastic_honey_cost = np.full(len(years), 185)  # Cost of packaged honey (single-use plastic)
        replace_interval_single_use_plastic_honey = 1  # Number of years before replacement
        replacement_cost_single_use_plastic_honey = 185  # Cost of replacement
        for i in range(replace_interval_single_use_plastic_honey, len(years), replace_interval_single_use_plastic_honey):
            single_use_plastic_honey_cost[i:] += replacement_cost_single_use_plastic_honey

        
        # Create the cost savings comparison line plot
        categories = ['Rietjes', 'Honing']  # Productcategorieën
        selected_category = st.selectbox("Selecteer Categorie", categories)

        if selected_category == 'Rietjes':
            data = pd.DataFrame({
                'Jaren': years,
                'Herbruikbare Niet-Plastic Rietjes': multi_use_non_plastic_straws_cost,
                'Herbruikbare Plastic Rietjes': multi_use_plastic_straws_cost,
                'Wegwerp Niet-Plastic Rietjes': single_use_non_plastic_straws_cost,
                'Wegwerp Plastic Rietjes': single_use_plastic_straws_cost
            })
        elif selected_category == 'Honing':
            data = pd.DataFrame({
                'Jaren': years,
                'Herbruikbare Niet-Plastic Honing': multi_use_non_plastic_honey_cost,
                'Herbruikbare Plastic Honing': multi_use_plastic_honey_cost,
                'Wegwerp Niet-Plastic Honing': single_use_non_plastic_honey_cost,
                'Wegwerp Plastic Honing': single_use_plastic_honey_cost
            })

        selected_data = data[['Jaren', f'Herbruikbare Niet-Plastic {selected_category}', f'Herbruikbare Plastic {selected_category}', f'Wegwerp Niet-Plastic {selected_category}', f'Wegwerp Plastic {selected_category}']]

        fig = px.line(selected_data, x='Jaren', y=[f'Herbruikbare Niet-Plastic {selected_category}', f'Herbruikbare Plastic {selected_category}',
                                                    f'Wegwerp Niet-Plastic {selected_category}', f'Wegwerp Plastic {selected_category}'],
                      title=f'Kostenbesparingen Vergelijking: {selected_category} - Plastic vs. Duurzame Alternatieven')
        fig.update_layout(xaxis_title='Jaren', yaxis_title='Kosten')
        st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function
        
        st.write("Hier is een uitleg over hoe de plot kan worden geïmplementeerd met echte gegevens:")
        st.write("1. Verzamel echte gegevens over de kosten van verschillende producttypen, zoals de prijs van plastic en duurzame alternatieven, inclusief het initiële investeringsbedrag en eventuele vervangingskosten.")
        st.write("2. Organiseer de gegevens in een tabel met jaren en kostenkolommen voor elk producttype.")
        st.write("3. Gebruik de 'px.line' functie van Plotly Express om een lijngrafiek te maken met de jaren op de x-as en de kosten op de y-as.")
        st.write("4. Pas de grafiek aan met de juiste labels voor de x- en y-assen, evenals een titel die het onderwerp van de kostenbesparingen beschrijft.")
        st.write("5. Gebruik de 'st.plotly_chart' functie van Streamlit om de grafiek weer te geven op de pagina.")
        
        st.write("---")
        
        st.subheader("Milieueffect Vergelijking: Plastic vs. Duurzame Verpakkingen")
        st.write("Deze plot toont een vergelijking van het milieueffect tussen verschillende verpakkingsopties voor honing en rietjes. Het helpt je om de mogelijke milieu-impact van verschillende materialen en gebruiksscenario's te begrijpen.")
        
        if selected_category == 'Rietjes':
            environmental_impact_data = pd.DataFrame({
                'Verpakkingsopties': ['Plastic', 'Duurzaam'],
                'CO2-uitstoot (ton)': [10, 5],
                'Afvalproductie (kg)': [100, 50],
                'Materiaalgebruik (kg)': [200, 100]
            })
        elif selected_category == 'Honing':
            environmental_impact_data = pd.DataFrame({
                'Verpakkingsopties': ['Plastic', 'Duurzaam'],
                'CO2-uitstoot (ton)': [5, 2],
                'Afvalproductie (kg)': [50, 20],
                'Materiaalgebruik (kg)': [100, 40]
            })

        fig = go.Figure()

        for column in environmental_impact_data.columns[1:]:
            fig.add_trace(go.Bar(
                x=environmental_impact_data['Verpakkingsopties'],
                y=environmental_impact_data[column],
                name=column
            ))

        fig.update_layout(
            xaxis_title="Verpakkingsopties",
            yaxis_title="Milieueffect",
            title=f"Milieueffecten van Verpakkingsopties - {selected_category}",
            showlegend=True
        )

        st.plotly_chart(fig)

        st.write("Hier is een uitleg over hoe de grafiek kan worden geïmplementeerd met echte gegevens:")
        st.write("1. Verzamel echte gegevens over het milieueffect van verschillende verpakkingsopties, zoals CO2-uitstoot, afvalproductie en materiaalgebruik.")
        st.write("2. Organiseer de gegevens in een tabel met de verpakkingsopties en de bijbehorende effecten.")
        st.write("3. Gebruik de `go.Bar` trace om de gegevens weer te geven in een staafgrafiek.")
        st.write("4. Voeg elke trace toe aan de `Figure` en stel de gewenste instellingen in voor de layout.")
        st.write("5. Gebruik `st.plotly_chart` om de grafiek in Streamlit weer te geven.")


    else:
        st.write("Er zijn nog geen formulierreacties gevonden voor de huidige gebruiker.")
