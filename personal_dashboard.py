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
    else:
        st.write("No form responses found.")

