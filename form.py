import streamlit as st
import numpy as np
import utils

def form_page(current_user_email):
    st.header("Formulier Pagina")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Form inputs
    inputs = [
        ("rietjes", "Gebruik je 'rietjes'?"),
        ("honingstaafjes", "Gebruik je 'honingstaafjes'?"),
        ("melkcupjes", "Gebruik je 'melkcupjes'?"),
        ("suikerzakjes", "Gebruik je 'suikerzakjes (met plastic coating)'?"),
        ("koekjeswrappers", "Gebruik je 'koekjeswrappers'?"),
        ("theezakjes_verpakking", "Gebruik je 'theezakjes + verpakking'?"),
        ("ontbijt_boter", "Gebruik je 'ontbijt (boter)'?"),
        ("ontbijt_jam_pindakaas_chocoladepasta", "Gebruik je 'ontbijt (jam, pindakaas, chocoladepasta)'?"),
        ("saus_mayonaise", "Gebruik je 'saus (mayonaise)'?"),
        ("saus_ketchup", "Gebruik je 'saus (ketchup)'?"),
        ("saus_mosterd", "Gebruik je 'saus (mosterd)'?"),
        ("saus_soya_saus", "Gebruik je 'saus (soya-saus)'?"),
        ("pepermuntverpakking", "Gebruik je 'pepermuntverpakking (plastic)'?"),
        ("snoepjes_rekening", "Gebruik je 'snoepjes (bij aanbieden rekening)'?"),
        ("tandenstokerverpakking", "Gebruik je 'tandenstokerverpakking (plastic)'?"),
        ("stampers", "Gebruik je 'stampers'?"),
        ("wegwerpbekers_feesten_partijen", "Gebruik je 'wegwerpbekers (feesten en partijen)'?"),
        ("ijsjes_plastic_verpakking", "Gebruik je 'ijsjes (met plastic verpakking)'?"),
        ("natte_doekjes_garnalen_spareribs", "Gebruik je 'natte doekjes (na garnalen/spare-ribs)'?")
    ]

    responses = {"Email": current_user_email}  # Add current user's email to responses

    for i, (category, question) in enumerate(inputs):
        uses_category = st.selectbox(question, ("Nee", "Ja"), key=f"{category}_selectbox_{i}")
        responses[category] = uses_category
        product_category = st.selectbox("Onder welke categorie valt dit product?", ("Multi-Use Non-Plastics", "Single-Use Non-Plastics", "n.v.t. (product uit assortiment gehaald)", "Single-Use Plastics (alleen kiezen wanneer 'Ja' is geantwoord)"), key=f"{category}_alternative_{i}")
        responses[f"product_category_{category}"] = product_category

        if product_category != "n.v.t. (product uit assortiment gehaald)":
            aantal_category = st.number_input(f"Hoeveel {category}s gebruik je per jaar?", min_value=0, step=1)
            prijs_per_category = st.number_input(f"Wat is de prijs per {category}?", min_value=0.0, step=0.01)
            responses[f"aantal_{category}s"] = aantal_category
            responses[f"prijs_per_{category}"] = prijs_per_category
        else:
            responses[f"aantal_{category}s"] = np.nan
            responses[f"prijs_per_{category}"] = np.nan

        if (i + 1) % 3 == 0 or i == len(inputs) - 1:
            st.markdown('</div>', unsafe_allow_html=True)

    submit_button = st.button("Verzenden")

    # Form submission handling
    if submit_button:
        utils.insert_form_responses(responses)
        st.success("Formulier succesvol verzonden!")
