import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def dev(current_user_email):
    st.header("Overzicht van jouw Duurzaamheidsinspanningen")
    st.write(f"Huidige gebruiker: {current_user_email}")

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

    # Replacement intervals for each category
    multi_use_non_plastics_replace_interval = 5
    single_use_non_plastics_replace_interval = 1
    multi_use_plastics_replace_interval = 3
    single_use_plastics_replace_interval = 1

    # Generate sample data for cost comparison
    years = np.arange(1, 11)  # Years 1 to 10

    # Calculate cost per year for each category
    single_use_plastic_cost = single_use_plastics_cost[categories.index(selected_category)]
    multi_use_non_plastic_cost = multi_use_non_plastics_cost[categories.index(selected_category)]
    multi_use_plastic_cost = multi_use_plastics_cost[categories.index(selected_category)]
    single_use_non_plastics_cost = single_use_non_plastics_cost[categories.index(selected_category)]

    single_use_plastic_cost_per_year = [
        single_use_plastics_cost if year % single_use_plastics_replace_interval == 0 else 0
        for year in years
    ]


    multi_use_non_plastic_cost_per_year = [
        multi_use_non_plastics_cost * np.ceil(year / multi_use_non_plastics_replace_interval)
        if year % multi_use_non_plastics_replace_interval == 0
        else multi_use_non_plastics_cost
        for year in years
    ]

    multi_use_plastic_cost_per_year = [
        multi_use_plastics_cost * np.ceil(year / multi_use_plastics_replace_interval)
        if year % multi_use_plastics_replace_interval == 0
        else multi_use_plastics_cost
        for year in years
    ]

    single_use_non_plastics_cost_per_year = np.repeat(single_use_non_plastics_cost, len(years))

    # Create the cost savings comparison line plot
    data = pd.DataFrame({
        'Years': years,
        'Single-Use Plastics': single_use_plastic_cost_per_year,
        'Multi-Use Non-Plastics': multi_use_non_plastic_cost_per_year,
        'Multi-Use Plastics': multi_use_plastic_cost_per_year,
        'Single-Use Non-Plastics': single_use_non_plastics_cost_per_year
    })

    selected_data = data[
        ['Years', 'Single-Use Plastics', 'Multi-Use Non-Plastics', 'Multi-Use Plastics', 'Single-Use Non-Plastics']
    ]

    fig = px.line(selected_data, x='Years',
                  y=['Single-Use Plastics', 'Multi-Use Non-Plastics', 'Multi-Use Plastics', 'Single-Use Non-Plastics'],
                  title='Cost Savings Comparison: Plastic vs. Sustainable Alternatives')
    fig.update_layout(xaxis_title='Years', yaxis_title='Cost ($)')
    st.plotly_chart(fig)  # Display the plot using Streamlit's `st.plotly_chart` function
