import streamlit as st
import pandas as pd
import numpy as np
import os
import utils
from decimal import Decimal

def form_page(current_user_email):
    st.header("Formulier Pagina")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Form inputs
    inputs = [
        ("rietjes", "Gebruik je plastic 'rietjes'?"),
        ("honingstaafjes", "Gebruik je plastic 'honingstaafjes'?"),
        ("melkcupjes", "Gebruik je plastic 'melkcupjes'?"),
        ("suikerzakjes", "Gebruik je plastic 'suikerzakjes'?"),
        ("koekjeswrappers", "Gebruik je koekjes verpakt in plastic'?"),
        ("theezakjes_verpakking", "Gebruik je 'theezakjes in plastic verpakking'?"),
        ("ontbijt_boter", "Gebruik je boter in plastic verpakking?"),
        ("ontbijt_jam_pindakaas_chocoladepasta", "Gebruik je 'jam, pindakaas, chocoladepasta' en dergelijke in plastic verpakking?"),
        ("saus_mayonaise", "Gebruik je 'mayonaise' geserveerd in plastic bakjes?"),
        ("saus_ketchup", "Gebruik je 'ketchup' geserveerd in plastic bakjes?"),
        ("saus_mosterd", "Gebruik je 'mosterd' geserveerd in plastic bakjes?"),
        ("saus_soya_saus", "Gebruik je 'soya saus' geserveerd in plastic bakjes?"),
        ("pepermuntverpakking", "Gebruik je 'pepermunt in plastic verpakking' (bij aanbieden rekening)?"),
        ("snoepjes_rekening", "Gebruik je 'snoepjes in plastic verpakking' (bij aanbieden rekening)?"),
        ("tandenstokerverpakking", "Gebruik je 'tandenstokers in plastic verpakking'?"),
        ("stampers", "Gebruik je plastic 'stampers'?"),
        ("wegwerpbekers_feesten_partijen", "Gebruik je plastic 'wegwerpbekers (feesten en evenementen)'?"),
        ("ijsjes_plastic_verpakking", "Gebruik je 'ijsjes met plastic verpakking'?"),
        ("natte_doekjes_garnalen_spareribs", "Gebruik je 'alcohol/schoonmaak doekjes in plastic verpakking' (na garnalen/spare-ribs)?")
    ]

    responses = {"Email": current_user_email}  # Add current user's email to responses

    for i, (category, question) in enumerate(inputs):
        uses_category = st.selectbox(question, ("Nee", "Ja"), key=f"{category}_selectbox_{i}")
        responses[category] = uses_category
        product_category = st.selectbox("Onder welke categorie valt dit product?", ("Multi-Use Non-Plastics", "Single-Use Non-Plastics", "n.v.t. (product uit assortiment gehaald)", "Single-Use Plastics (alleen kiezen wanneer 'Ja' is geantwoord)"), key=f"{category}_alternative_{i}")
        responses[f"product_category_{category}"] = product_category

        if product_category != "n.v.t. (product uit assortiment gehaald)":
            aantal_category = st.number_input(f"Hoeveel {category} gebruik je per jaar?", min_value=0, step=100)
            prijs_per_category = st.number_input(f"Wat is de prijs per {category}?", min_value=0.0, step=0.01)
            responses[f"aantal_{category}"] = aantal_category
            responses[f"prijs_per_{category}"] = prijs_per_category
        else:
            responses[f"aantal_{category}"] = np.nan
            responses[f"prijs_per_{category}"] = np.nan

        if (i + 1) % 3 == 0 or i == len(inputs) - 1:
            st.markdown('</div>', unsafe_allow_html=True)

    submit_button = st.button("Verzenden")

    # Form submission handling
    if submit_button:
        utils.insert_form_responses(responses)
        st.success("Formulier succesvol verzonden!")
