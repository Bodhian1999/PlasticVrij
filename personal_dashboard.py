import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import get_user_email, get_user_score, get_recent_form_response

def personal_dashboard_page(current_user_email):
    st.header("Persoonlijk Dashboard")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    column_names = [
    'id',
    'created_at',
    'email',
    'rietjes',
    'honingstaafjes',
    'melkcupjes',
    'suikerzakjes',
    'koekjeswrappers',
    'theezakjes_verpakking',
    'ontbijt_boter',
    'ontbijt_jam_pindakaas_chocoladepasta',
    'saus_mayonaise',
    'saus_ketchup',
    'saus_mosterd',
    'saus_soya_saus',
    'pepermuntverpakking',
    'snoepjes_rekening',
    'tandenstokerverpakking',
    'stampers',
    'wegwerpbekers_feesten_partijen',
    'ijsjes_plastic_verpakking',
    'natte_doekjes_garnalen_spareribs',
    'chosen_alternative_rietjes',
    'chosen_alternative_honingstaafjes',
    'chosen_alternative_melkcupjes',
    'chosen_alternative_suikerzakjes',
    'chosen_alternative_koekjeswrappers',
    'chosen_alternative_theezakjes_verpakking',
    'chosen_alternative_ontbijt_boter',
    'chosen_alternative_ontbijt_jam_pindakaas_chocoladepasta',
    'chosen_alternative_saus_mayonaise',
    'chosen_alternative_saus_ketchup',
    'chosen_alternative_saus_mosterd',
    'chosen_alternative_saus_soya_saus',
    'chosen_alternative_pepermuntverpakking',
    'chosen_alternative_snoepjes_rekening',
    'chosen_alternative_tandenstokerverpakking',
    'chosen_alternative_stampers',
    'chosen_alternative_wegwerpbekers_feesten_partijen',
    'chosen_alternative_ijsjes_plastic_verpakking',
    'chosen_alternative_natte_doekjes_garnalen_spareribs',
    'aantal_rietjes',
    'aantal_honingstaafjes',
    'aantal_melkcupjes',
    'aantal_suikerzakjes',
    'aantal_koekjeswrappers',
    'aantal_theezakjes_verpakking',
    'aantal_ontbijt_boter',
    'aantal_ontbijt_jam_pindakaas_chocoladepasta',
    'aantal_saus_mayonaise',
    'aantal_saus_ketchup',
    'aantal_saus_mosterd',
    'aantal_saus_soya_saus',
    'aantal_pepermuntverpakking',
    'aantal_snoepjes_rekening',
    'aantal_tandenstokerverpakking',
    'aantal_stampers',
    'aantal_wegwerpbekers_feesten_partijen',
    'aantal_ijsjes_plastic_verpakking',
    'aantal_natte_doekjes_garnalen_spareribs',
    'prijs_per_rietjes',
    'prijs_per_honingstaafjes',
    'prijs_per_melkcupjes',
    'prijs_per_suikerzakjes',
    'prijs_per_koekjeswrappers',
    'prijs_per_theezakjes_verpakking',
    'prijs_per_ontbijt_boter',
    'prijs_per_ontbijt_jam_pindakaas_chocoladepasta',
    'prijs_per_saus_mayonaise',
    'prijs_per_saus_ketchup',
    'prijs_per_saus_mosterd',
    'prijs_per_saus_soya_saus',
    'prijs_per_pepermuntverpakking',
    'prijs_per_snoepjes_rekening',
    'prijs_per_tandenstokerverpakking',
    'prijs_per_stampers',
    'prijs_per_wegwerpbekers_feesten_partijen',
    'prijs_per_ijsjes_plastic_verpakking',
    'prijs_per_natte_doekjes_garnalen_spareribs']

    # Load the most recent form response from the database
    recent_response = get_recent_form_response(current_user_email)

    if recent_response:
        # Convert the response to a pandas DataFrame for easy table display
        df = pd.DataFrame([recent_response],  columns=column_names)

        # Display the table
        st.dataframe(df)
    else:
        st.write("Er zijn geen recente formuliern reacties gevonden voor deze gebruiker.")

