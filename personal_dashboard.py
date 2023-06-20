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
        
        # Select the columns representing the categories
        category_columns = ['rietjes', 'honingstaafjes', 'melkcupjes', 'suikerzakjes', 'koekjeswrappers',
                            'theezakjes_verpakking', 'ontbijt_boter', 'ontbijt_jam_pindakaas_chocoladepasta',
                            'saus_mayonaise', 'saus_ketchup', 'saus_mosterd', 'saus_soya_saus',
                            'pepermuntverpakking', 'snoepjes_rekening', 'tandenstokerverpakking',
                            'stampers', 'wegwerpbekers_feesten_partijen', 'ijsjes_plastic_verpakking',
                            'natte_doekjes_garnalen_spareribs']

        # Count the "Yes" and "No" answers for each category
        counts = form_responses_df[category_columns].apply(pd.value_counts)

        # Plot the bar chart
        fig, ax = plt.subplots()
        counts.plot(kind='bar', ax=ax)
        ax.set_xlabel('Category')
        ax.set_ylabel('Count')
        ax.set_title('Count of Yes vs No Answers for Each Category')
        st.pyplot(fig)
    else:
        st.write("No form responses found.")
        
        

