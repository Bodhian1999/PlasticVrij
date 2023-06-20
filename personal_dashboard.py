import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import calculate_non_plastics_percentage, get_user_score, get_recent_form_response, get_all_form_responses

def personal_dashboard_page(current_user_email):

    st.header("Persoonlijk Dashboard")
    st.write(f"Huidige gebruiker: {current_user_email}")

    form_responses_df = get_all_form_responses(current_user_email)
    
    if form_responses_df is not None:
        st.dataframe(form_responses_df)
        # Get unique values from the 'created_at' column
        created_at_values = form_responses_df['created_at'].unique()

        # Select the row based on the user's choice of 'created_at'
        selected_created_at = st.selectbox('Select a date:', created_at_values)

        # Filter the DataFrame to get the selected row
        selected_row = form_responses_df[form_responses_df['created_at'] == selected_created_at]

        # Select the columns representing the categories
        category_columns = ['rietjes', 'honingstaafjes', 'melkcupjes', 'suikerzakjes', 'koekjeswrappers',
                            'theezakjes_verpakking', 'ontbijt_boter', 'ontbijt_jam_pindakaas_chocoladepasta',
                            'saus_mayonaise', 'saus_ketchup', 'saus_mosterd', 'saus_soya_saus',
                            'pepermuntverpakking', 'snoepjes_rekening', 'tandenstokerverpakking',
                            'stampers', 'wegwerpbekers_feesten_partijen', 'ijsjes_plastic_verpakking',
                            'natte_doekjes_garnalen_spareribs']

        # Count the "Yes" and "No" answers for each category in the selected row
        counts = selected_row[category_columns].apply(pd.value_counts)

        # Plot the bar chart
        fig, ax = plt.subplots()
        counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Category')
        ax.set_ylabel('Count')
        ax.set_title('Count of Yes vs No Answers for Each Category (Selected Row)')
        st.pyplot(fig)
    else:
        st.write("No form responses found.")
        
        

