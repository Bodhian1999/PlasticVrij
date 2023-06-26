import streamlit as st
import pandas as pd
import numpy as np
import os
import utils
from decimal import Decimal
from utils import get_recent_form_response

def home_page(current_user_email):
    st.header("Welkom!")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")