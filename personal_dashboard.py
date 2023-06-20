import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import get_recent_form_response

def personal_dashboard_page(current_user_email):

    st.header("Persoonlijk Dashboard")
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Load the most recent form response from the database
    recent_response = get_recent_form_response(current_user_email)

    if recent_response:
        # Print the recent response
        st.write("Recente respons:")
        st.write(recent_response)
    else:
        st.write("Er is geen recente respons beschikbaar.")

