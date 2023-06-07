import streamlit as st
from auth import auth_page
from form import form_page
from personal_dashboard import personal_dashboard_page
from general_dashboard import general_dashboard_page

def main():
    st.title("Gebruikersauthenticatie App")

    # Store login state and current user
    is_logged_in = st.session_state.get('is_logged_in', False)
    current_user_email = st.session_state.get('current_user_email', '')

    if not is_logged_in:
        auth_page(is_logged_in)  # Pass the initial login state as is_logged_in
        if not st.session_state.get('current_user_email'):
            return

        # Update the login state and current user
        st.session_state['is_logged_in'] = True
        st.session_state['current_user_email'] = current_user_email

    # Add sidebar to all pages except the login page
    if is_logged_in:
        page = st.sidebar.selectbox("Selecteer Pagina", ("Formulier Pagina", "Persoonlijk Dashboard", "Algemeen Dashboard"))

        if page == "Persoonlijk Dashboard":
            personal_dashboard_page(current_user_email)
        elif page == "Algemeen Dashboard":
            general_dashboard_page()
        elif page == "Formulier Pagina":
            form_page(current_user_email)

        # Logout button in the sidebar
        logout_button = st.sidebar.button("Uitloggen")
        if logout_button:
            # Clear the session state
            st.session_state.clear()

            # Redirect to the login page by modifying URL parameters
            st.experimental_set_query_params()
            return

if __name__ == "__main__":
    main()
