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
        ("rietjes", "Gebruik je 'rietjes'?"),
        ("honingstaafjes", "Gebruik je 'honingstaafjes'?"),
        ("melkcupjes", "Gebruik je 'melkcupjes'?"),
        ("suikerzakjes", "Gebruik je 'suikerzakjes'?"),
        ("koekjeswrappers", "Serveer je koekjes?"),
        ("theezakjes_verpakking", "Serveer je thee?"),
        ("ontbijt_boter", "Serveer je boter?"),
        ("ontbijt_jam_pindakaas_chocoladepasta", "Serveer je 'jam, pindakaas, chocoladepasta' en dergelijke?"),
        ("saus_mayonaise", "Serveer je 'mayonaise'?"),
        ("saus_ketchup", "Serveer je 'ketchup'?"),
        ("saus_mosterd", "Serveer je 'mosterd'?"),
        ("saus_soya_saus", "Serveer je 'soya saus'?"),
        ("pepermuntverpakking", "Serveer je 'pepermunt' (bij aanbieden rekening)?"),
        ("snoepjes_rekening", "Serveer je 'snoepjes' (bij aanbieden rekening)?"),
        ("tandenstokerverpakking", "Bied je 'tandenstokers' aan?"),
        ("stampers", "Gebruik je 'stampers'?"),
        ("wegwerpbekers_feesten_partijen", "Gebruik je 'bekers (feesten en evenementen)'?"),
        ("ijsjes_plastic_verpakking", "verkoop je 'ijsjes met verpakking'?"),
        ("natte_doekjes_garnalen_spareribs", "bied je 'alcohol/schoonmaak doekjes' aan (na garnalen/spare-ribs)?")
    ]

    responses = {"Email": current_user_email}  # Add current user's email to responses

    for i, category in enumerate(categories):
        st.subheader(f"{category}")

        uses_category = st.selectbox("Do you use this category?", ("No", "Yes"), key=f"{category}_selectbox_{i}")
        responses[category] = uses_category

        if uses_category == "Yes":
            product_category = st.selectbox(
                "Under which category does this product belong?",
                (
                    "Multi-Use Non-Plastics",
                    "Single-Use Non-Plastics",
                    "Single-Use Plastics (only select if 'Yes' is answered)",
                ),
                key=f"{category}_alternative_{i}",
            )
            responses[f"product_category_{category}"] = product_category

            if product_category != "n.v.t. (product uit assortiment gehaald)":
                aantal_category = st.number_input(
                    f"How many {category} do you use per year?",
                    min_value=0,
                    step=100,
                    key=f"{category}_amount_{i}",
                )
                prijs_per_category = st.number_input(
                    f"What is the price per {category}?",
                    min_value=0.0,
                    step=0.01,
                    key=f"{category}_price_{i}",
                )
                responses[f"aantal_{category}"] = aantal_category
                responses[f"prijs_per_{category}"] = prijs_per_category
            else:
                responses[f"aantal_{category}"] = np.nan
                responses[f"prijs_per_{category}"] = np.nan
        else:
            responses[f"product_category_{category}"] = "n.v.t. (product uit assortiment gehaald)"
            responses[f"aantal_{category}"] = np.nan
            responses[f"prijs_per_{category}"] = np.nan

        if (i + 1) % 3 == 0 or i == len(categories) - 1:
            st.markdown("</div>", unsafe_allow_html=True)

    submit_button = st.button("Submit")

    # Form submission handling
    if submit_button:
        # Process the responses
        # utils.insert_form_responses(responses)
        st.success("Form successfully submitted!")