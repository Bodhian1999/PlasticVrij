import streamlit as st
from utils import verify_user, create_user_account, hash_password

def register_page():
    st.header("Create an Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    postal_code = st.text_input("Postal Code")
    company_name = st.text_input("Company Name")
    register_button = st.button("Register")

    if register_button:
        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        utils.create_user_account(username, email, password, postal_code, company_name)
        st.success("Account created successfully! You can now log in.")

if __name__ == "__main__":
    register_page()
