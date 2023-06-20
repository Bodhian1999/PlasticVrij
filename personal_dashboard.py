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

        # Initialize the counts
        ja_count = 0
        nee_count = 0

        # Loop over the columns between index 2 and 23
        for column in selected_row.columns[2:24]:
            if selected_row[column].values[0] == 'Ja':
                ja_count += 1
            elif selected_row[column].values[0] == 'Nee':
                nee_count += 1

        # Create a DataFrame with the counts
        counts_df = pd.DataFrame({'Answer': ['Ja', 'Nee'], 'Count': [ja_count, nee_count]})

        # Plot the bar chart
        fig, ax = plt.subplots()
        counts_df.plot(x='Answer', y='Count', kind='bar', ax=ax)
        ax.set_xlabel('Answer')
        ax.set_ylabel('Count')
        ax.set_title('Total Count of Ja vs Nee for All Categories (Selected Row)')
        st.pyplot(fig)
        
        # Assuming you have the DataFrame `form_responses_df`

        for idx, column in enumerate(form_responses_df.columns):
            print(f"Index: {idx}, Column: {column}")

    else:
        st.write("No form responses found.")
        
        

