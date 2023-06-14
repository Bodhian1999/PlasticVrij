import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import get_user_email, get_user_score

def calculate_non_plastics_percentage(df):
    # Calculate the percentage of 'Non-Plastics' in the fourth visual
    non_plastics_count = df.iloc[:, 1:].eq('Non-Plastics').sum().sum()
    total_count = df.iloc[:, 1:].notnull().sum().sum()
    non_plastics_percentage = non_plastics_count / total_count

    return non_plastics_percentage

def personal_dashboard_page(current_user_email):
    st.header("Peroonlijk Dashboard")

    # Display the active user's email
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Load form responses from the database
    df = pd.read_csv('form_responses.csv')

    # Calculate non-plastics percentage
    non_plastics_percentage = calculate_non_plastics_percentage(df)

    # Calculate user score and average score
    user_score, avg_score = get_user_score(username, non_plastics_percentage)

    # Describe the first visual - score comparison
    st.header('Vergelijking van jouw Non-Plastics score in vergelijking met de rest')
    st.write('Deze visualisatie vergelijkt jouw Non-Plastics score met het gemiddelde van alle andere gebruikers. Deze score is gebaseerd op de hoeveelheid verschillende soorten Single-Use Plastic producten die je gebruikt en hangt daar een score aan: hoe minder hoe beter natuurlijk. De blauwe gestippelde lijn vertegenwoordigt jouw score, terwijl de zwarte gestippelde lijn het gemiddelde van de rest van de gebruikers weergeeft. Dit helpt je om je eigen prestaties te begrijpen en vergelijken met de algemene scores van anderen.')

    # Adjust user score based on non-plastics percentage
    user_score_adjusted = max(user_score, non_plastics_percentage * 10)

    # Create a new figure and subplot with a specified size
    fig, ax = plt.subplots(figsize=(6, 1))

    # Add a vertical line at the x-coordinate specified by user_score_adjusted
    ax.axvline(x=user_score_adjusted, color='blue', linestyle='--', label='Jij')

    # Add a vertical line at the x-coordinate specified by avg_score
    ax.axvline(x=avg_score, color='black', linestyle='--', label='Rest')

    # Set the limits of the x-axis
    ax.set_xlim(0, 10)

    # Set the title of the plot
    ax.set_title("Vergelijking van jouw Non-Plastics score in vergelijking met de rest")

    # Add a legend to the plot
    ax.legend(fontsize='small', loc='upper left')

    # Hide the y-axis and its labels
    ax.yaxis.set_visible(False)

    # Set the tick parameters for both x and y axes
    ax.tick_params(axis='both', which='major', labelsize=8)

    # Display the plot using Streamlit
    st.pyplot(fig)

    # Display the scores under the visual score bar
    st.write("Jouw score: ", round(user_score_adjusted, 2))
    st.write("Gemiddelde score: ", round(avg_score, 2))

    # Describe the second visual - overall usage
    st.header('Overzicht van je totale Single-Use Plastic gebruik')
    st.write('Deze visualisatie toont een overzicht van je totale Single-Use Plastic gebruik. Het toont het percentage van elk type Single-Use Plastic product dat je hebt gebruikt.')

    # Calculate the total count for each product type
    product_counts = df.iloc[:, 1:].value_counts(normalize=True) * 100

    # Create a bar chart for the product counts
    fig, ax = plt.subplots(figsize=(8, 4))
    product_counts.plot(kind='bar', ax=ax, color='orange')

    # Set the title and labels for the bar chart
    ax.set_title("Overzicht van je totale Single-Use Plastic gebruik")
    ax.set_xlabel("Type product")
    ax.set_ylabel("Percentage")

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the plot using Streamlit
    st.pyplot(fig)

    # Describe the third visual - product count comparison
    st.header('Vergelijking van je gebruik per type product')
    st.write('Deze visualisatie vergelijkt je gebruik van elk type product met het gemiddelde van alle andere gebruikers. De blauwe balkjes vertegenwoordigen jouw gebruik, terwijl de oranje balkjes het gemiddelde gebruik van de rest van de gebruikers weergeven.')

    # Calculate the average count for each product type
    avg_product_counts = df.iloc[:, 1:].apply(lambda x: x.value_counts(normalize=True).mean() * 100)

    # Create a bar chart for the product count comparison
    fig, ax = plt.subplots(figsize=(8, 4))
    width = 0.35
    x = np.arange(len(product_counts))
    user_bars = ax.bar(x, product_counts, width, label='Jij', color='blue')
    avg_bars = ax.bar(x + width, avg_product_counts, width, label='Rest', color='orange')

    # Set the title and labels for the bar chart
    ax.set_title("Vergelijking van je gebruik per type product")
    ax.set_xlabel("Type product")
    ax.set_ylabel("Percentage")

    # Set the x-axis tick positions and labels
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(product_counts.index)

    # Add a legend to the plot
    ax.legend()

    # Display the plot using Streamlit
    st.pyplot(fig)

    # Describe the fourth visual - non-plastics percentage
    st.header('Percentage Non-Plastics')
    st.write('Deze visualisatie toont het percentage van "Non-Plastics" items in je totale gebruik. Dit helpt je om je prestaties in het verminderen van Single-Use Plastics te meten.')

    # Create a pie chart for the non-plastics percentage
    fig, ax = plt.subplots(figsize=(6, 4))
    labels = ['Non-Plastics', 'Plastics']
    sizes = [non_plastics_percentage * 100, (1 - non_plastics_percentage) * 100]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['orange', 'blue'])
    ax.axis('equal')

    # Set the title of the pie chart
    ax.set_title("Percentage Non-Plastics")

    # Display the plot using Streamlit
    st.pyplot(fig)
