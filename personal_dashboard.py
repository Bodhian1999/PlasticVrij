import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import get_user_email, get_user_score, get_recent_form_response

def personal_dashboard_page(current_user_email):
    st.header("Persoonlijk Dashboard")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Load the most recent form response from the database
    recent_response = get_recent_form_response(current_user_email)

    if recent_response:
        # Convert the response to a pandas DataFrame for easy table display
        df = pd.DataFrame(recent_response, columns=['id', 'created_at', 'email', 'rietjes', 'honingstaafjes', ...])

        # Display the table
        st.dataframe(df)
    else:
        st.write("Er zijn geen recente formuliern reacties gevonden voor deze gebruiker.")

