import streamlit as st
import pandas as pd
import numpy as np
import os
import utils
from decimal import Decimal
from utils import get_recent_form_response

def get_previous_product_category_index(category, previous_response_df):
    categories = [
        "Multi-Use Non-Plastics",
        "Single-Use Non-Plastics",
        "Multi-Use plastics",
        "Single-Use Plastics",
    ]
    previous_category_value = previous_response_df[f"product_category_{category}"].values[0]
    if previous_category_value in categories:
        return categories.index(previous_category_value)
    else:
        return 0

def form_page(current_user_email):
    st.title("Duurzaamheidsformulier")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    st.write("Vul het onderstaande formulier in om je duurzaamheidsgegevens in te voeren.")
    st.write("Indien je het formulier al eerder hebt ingevuld worden de waarden die je toen hebt opgegeven in het formulier getoond zodat je enkel de waarden die je wil bijwerken hoeft aan te passen.")
    st.write("Je kunt het formulier zo vaak invullen als je wil. Je eerdere reacties zijn beschikbaar in jouw persoonlijke dashboard.")
    
    previous_response_df = get_recent_form_response(current_user_email)
    #st.dataframe(previous_response_df)

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
    
    for i, (category, question) in enumerate(inputs):
        uses_category = st.selectbox(
            question,
            ("Nee", "Ja"),
            key=f"{category}_selectbox_{i}",
            index=1 if previous_response_df is not None and previous_response_df.at[0, category] == "Ja" else 0,
        )
        responses[category] = uses_category

        if uses_category == "Ja":
            product_category = st.selectbox(
                "Onder welke categorie valt dit product?",
                (
                    "Multi-Use Non-Plastics",
                    "Single-Use Non-Plastics",
                    "Multi-Use plastics",
                    "Single-Use Plastics",
                ),
                key=f"{category}_alternative_{i}",
                index=get_previous_product_category_index(category, previous_response_df) if previous_response_df is not None else 0,
            )
            responses[f"product_category_{category}"] = product_category

            if previous_response_df is not None:
                previous_aantal = previous_response_df[f"aantal_{category}"].values[0]
                previous_prijs_per = previous_response_df[f"prijs_per_{category}"].values[0]
                aantal_category = st.number_input(
                    f"Hoeveel {category} gebruikt u per jaar?",
                    min_value=0,
                    step=100,
                    key=f"{category}_amount_{i}",
                    value=int(previous_aantal) if not pd.isnull(previous_aantal) else 0,
                )
                prijs_per_category = st.number_input(
                    f"Wat is de prijs per {category}?",
                    min_value=0.0,
                    step=0.01,
                    key=f"{category}_price_{i}",
                    value=float(previous_prijs_per) if not pd.isnull(previous_prijs_per) else 0.0,
                )
            else:
                aantal_category = st.number_input(
                    f"Hoeveel {category} gebruikt u per jaar?",
                    min_value=0,
                    step=100,
                    key=f"{category}_amount_{i}",
                )
                prijs_per_category = st.number_input(
                    f"Wat is de prijs per {category}?",
                    min_value=0.0,
                    step=0.01,
                    key=f"{category}_price_{i}",
                )

            responses[f"aantal_{category}"] = aantal_category
            responses[f"prijs_per_{category}"] = prijs_per_category
        else:
            responses[f"product_category_{category}"] = "n.v.t. (product uit assortiment gehaald)"
            responses[f"aantal_{category}"] = np.nan
            responses[f"prijs_per_{category}"] = np.nan

        if (i + 1) % 3 == 0 or i == len(inputs) - 1:
            st.markdown("</div>", unsafe_allow_html=True)

    submit_button = st.button("Verzenden")

    # Form submission handling
    if submit_button:
        # Process the responses
        utils.insert_form_responses(responses)
        st.success("Formulier succesvol verzonden!")