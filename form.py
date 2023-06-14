import streamlit as st
import numpy as np
import utils

def form_page(current_user_email):
    st.header("Formulier Pagina")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Form inputs
    inputs = [
        ("rietje", "Gebruik je plastic 'rietjes'?"),
        ("honingstaafje", "Gebruik je plastic 'honingstaafjes'?"),
        ("melkcupje", "Gebruik je plastic 'melkcupjes'?"),
        ("suikerzakje", "Gebruik je plastic 'suikerzakjes'?"),
        ("koekjeswrapper", "Gebruik je koekjes verpakt in plastic'?"),
        ("plastic_theezakje", "Gebruik je 'theezakjes in plastic verpakking'?"),
        ("botercupje", "Gebruik je boter in plastic verpakking?"),
        ("jam_pindakaas_chocoladepasta", "Gebruik je 'jam, pindakaas, chocoladepasta' en dergelijke in plastic verpakking?"),
        ("mayonaise_bakje", "Gebruik je 'mayonaise' geserveerd in plastic bakjes?"),
        ("ketchup_bakje", "Gebruik je 'ketchup' geserveerd in plastic bakjes?"),
        ("mosterd_bakje", "Gebruik je 'mosterd' geserveerd in plastic bakjes?"),
        ("soya_saus_bakje", "Gebruik je 'soya saus' geserveerd in plastic bakjes?"),
        ("pepermunt_wrapper", "Gebruik je 'pepermunt in plastic verpakking' (bij aanbieden rekening)?"),
        ("snoep_wrapper", "Gebruik je 'snoepjes in plastic verpakking' (bij aanbieden rekening)?"),
        ("tandenstoker_wrapper", "Gebruik je 'tandenstokers in plastic verpakking'?"),
        ("stamper", "Gebruik je plastic 'stampers'?"),
        ("wegwerpbeker", "Gebruik je plastic 'wegwerpbekers (feesten en evenementen)'?"),
        ("ijs_wrapper", "Gebruik je 'ijsjes met plastic verpakking'?"),
        ("alcohol_schoonmaak_doekje", "Gebruik je 'alcohol/schoonmaak doekjes in plastic verpakking' (na garnalen/spare-ribs)?")
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
