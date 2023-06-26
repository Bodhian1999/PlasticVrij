import streamlit as st

def home_page(current_user_email):
    st.header("Welkom!")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Add an inviting image or logo
    #st.image("path_to_image/logo.png", use_column_width=True)

    # Introduction
    st.write("Welkom bij ons plasticvrije terras-initiatief! Hier kun je jouw bijdrage aan het verminderen van plastic op terrassen volgen en delen. Ontdek je duurzaamheidsscore, vergelijk deze met andere ondernemers en zie de voortgang die we samen boeken!")
    
    # Add a hyperlink to the project's main website
    st.markdown("[Lees meer over het project en krijg tips voor plasticvrije terrassen](https://plasticvrijterras.com/)")

    # Add an image related to plastic-free terraces
    #st.image("path_to_image/plastic_free_terraces.jpg", use_column_width=True)

    # Explanation of the app
    st.write("Wat kun je doen op deze app?")
    st.write("- Vul het formulier in om jouw gebruik van plastic op het terras te registreren.")
    st.write("- Volg jouw duurzaamheidsscore en zie hoe deze zich verhoudt tot andere ondernemers.")
    st.write("- Bekijk de interactieve kaart en zie waar andere ondernemers zich bevinden.")
    st.write("- Blijf op de hoogte van de laatste ontwikkelingen op het gebied van plasticvrije terrassen.")

    # Add more visuals or images to illustrate the features and benefits of the app

    # Call-to-action
    st.write("Doe mee en maak jouw terras plasticvrij!")

    # Add a visually appealing image or illustration related to plastic-free terraces
    #st.image("path_to_image/plastic_free_terrace_illustration.jpg", use_column_width=True)
