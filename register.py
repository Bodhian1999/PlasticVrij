import streamlit as st
from utils import create_user_account

def register_page():
    st.header("Create an Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    register_button = st.button("Register")

    if register_button:
        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        create_user_account(username, email, password)
        st.success("Account created successfully! You can now log in.")
