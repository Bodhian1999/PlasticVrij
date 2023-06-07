# login.py
import streamlit as st
from utils import verify_user

def login_page(is_logged_in):
    st.header("Inloggen")

    st.markdown(
        """
        <style>
        .login-input label {
            color: #00ff00;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    email = st.text_input("E-mail", key="login-email")
    password = st.text_input("Wachtwoord", type="password", key="login-password")
    login_button = st.button("Inloggen")

    if is_logged_in:
        # Log uit
        st.session_state['is_logged_in'] = False
        st.session_state['current_user'] = ''
        st.success("Succesvol uitgelogd!")
    elif login_button:
        if verify_user(email, password):
            # Inloggen
            st.session_state['is_logged_in'] = True
            st.session_state['current_user_email'] = email
            st.experimental_rerun()  # Trigger a rerun of the app to redirect to form_page
        else:
            st.error("Ongeldige e-mail of wachtwoord.")

