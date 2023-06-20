import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils import calculate_non_plastics_percentage, get_user_score, get_recent_form_response

def personal_dashboard_page(current_user_email):

    st.header("Persoonlijk Dashboard")
    st.write(f"Huidige gebruiker: {current_user_email}")

    # Load the most recent form response from the database
    recent_response = get_recent_form_response(current_user_email)
    st.write(f"Huidige gebruiker: {recent_response}")

    if recent_response:
        # Access the DataFrame object within the dictionary
       # recent_response_df = recent_response['data']

        # Calculate non-plastics percentage
        non_plastics_percentage = calculate_non_plastics_percentage(recent_response)

        # Calculate user score and average score
        user_score, avg_score = get_user_score(current_user_email, non_plastics_percentage)

        # Describe the first visual - score comparison
        st.header('Vergelijking van jouw Non-Plastics score in vergelijking met de rest')
        st.write('Deze visualisatie vergelijkt jouw Non-Plastics score met het gemiddelde van alle andere gebruikers. Deze score is gebasseerd op de hoeveelheid verschillende soorten Single-Use Plastic producten die je gebruikt en hangt daar een score aan: hoe minder hoe beter natuurlijk. De blauwe gestippelde lijn vertegenwoordigt jouw score, terwijl de zwarte gestippelde lijn het gemiddelde van de rest van de gebruikers weergeeft. Dit helpt je om je eigen prestaties te begrijpen en vergelijken met de algemene scores van anderen.')

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
        st.write("Gemiddelde score van de anderen: ", round(avg_score, 2))

        # Describe the second visual - bar chart
        st.header('Absolute Verdeling van de Totaalhoeveelheid per Productcategorie')
        st.write('Dit staafdiagram toont de verdeling van de totale hoeveelheden over verschillende productcategorieën. Elke staaf vertegenwoordigt een productcategorie, en de hoogte van de staaf geeft de totaalhoeveelheid voor die categorie weer. Dit helpt je om inzicht te krijgen in welke categorieën de meeste absolute hoeveelheden zijn.')

        # Specify the email address for which you want to calculate the sums
        email_address = current_user_email

        # Get the unique product categories from the latest input
        categories = recent_response_df.filter(regex=r'^product_category_').columns

        # Create a new DataFrame to store the calculated sums
        sums_df = pd.DataFrame(columns=['Product Category', 'Total Amount'])

        # Iterate over the categories and calculate the sums
        for category in categories:
            amount_column = category.replace('product_category_', 'aantal_') + 's'
            category_sum = recent_response_df.groupby(category)[amount_column].sum().reset_index()
            category_sum.columns = ['Product Category', 'Total Amount']
            sums_df = pd.concat([sums_df, category_sum], ignore_index=True)

        # Remove rows with NaN values
        sums_df = sums_df.dropna()

        # Group by 'Product Category' and sum the 'Total Amount'
        sums_df = sums_df.groupby('Product Category')['Total Amount'].sum().reset_index()

        # Exclude 'n.v.t. (product uit assortiment gehaald)' category
        filtered_df_bar = sums_df[sums_df['Product Category'] != 'n.v.t. (product uit assortiment gehaald)'].copy()

        # Remove text between brackets in x-axis labels
        filtered_df_bar.loc[:, 'Product Category'] = filtered_df_bar['Product Category'].str.replace(r'\s*\([^)]*\)', '', regex=True)

        # Assign colors based on category endings
        colors = ['red' if category.endswith(' Plastics') else 'green' for category in filtered_df_bar['Product Category']]

        # Create a bar chart with custom colors
        fig, ax = plt.subplots()
        ax.bar(filtered_df_bar['Product Category'], filtered_df_bar['Total Amount'], color=colors)

        # Add labels and title
        ax.set_xlabel('Product Categorie')
        ax.set_ylabel('Totale Hoeveelheid')
        ax.set_title('Absolute Verdeling van de Totaalhoeveelheid per Productcategorie')

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)

        # Display the chart using Streamlit
        st.pyplot(fig)

        # Display the third visual - Pie chart categories
        st.header('Percentage van de Totaalhoeveelheden per Productcategorie')
        st.write('Dit taartdiagram visualiseert het percentage van de totaalhoeveelheden dat wordt toegeschreven aan elke productcategorie. De grootte van elke taartpunt geeft het relatieve aandeel van de categorie weer. De labels binnen elke taartpunt geven de productcategorieën aan, samen met het exacte percentage. Dit helpt je om inzicht te krijgen in welke categorieën de meeste relatieve hoeveelheden zijn.')

        # Exclude 'n.v.t. (product uit assortiment gehaald)' category
        filtered_df_pie = sums_df[sums_df['Product Category'] != 'n.v.t. (product uit assortiment gehaald)'].copy()

        # Remove text between brackets in x-axis labels
        filtered_df_pie['Product Category'] = filtered_df_pie['Product Category'].str.replace(r'\s*\([^)]*\)', '', regex=True)

        # Assign colors based on category endings
        colors = ['red' if category.endswith(' Plastics') else 'green' for category in filtered_df_pie['Product Category']]

        # Calculate the percentages
        filtered_df_pie['Percentage'] = (filtered_df_pie['Total Amount'] / filtered_df_pie['Total Amount'].sum()) * 100

        # Create a pie chart with custom colors
        fig, ax = plt.subplots()
        ax.pie(filtered_df_pie['Percentage'], labels=filtered_df_pie['Product Category'], autopct='%1.1f%%', colors=colors)

        # Add title
        ax.set_title('Percentage van de Totaalhoeveelheden per Productcategorie')

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')

        # Display the chart using Streamlit
        st.pyplot(fig)

        # Display the fourth visual - Pie chart (non-)plastic
        st.header('Percentage van de Plastics en Non-Plastics Totaalhoeveelheden')
        st.write('Dit taartdiagram toont de verdeling van de totaalhoeveelheden tussen plastics en non-plastics. Elke taartpunt vertegenwoordigt een categorie. De grootte van elke taartpunt geeft het percentage van de totaalhoeveelheden weer. Dit helpt je om een beter begrip te krijgen van de verhouding tussen plastics en non-plastics in termen van hun bijdrage aan de totaalhoeveelheden.')

        # Group green percentages together
        green_percentage = filtered_df_pie.loc[filtered_df_pie['Product Category'].str.contains('Non-Plastics'), 'Percentage'].sum()
        green_amount = filtered_df_pie.loc[filtered_df_pie['Product Category'].str.contains('Non-Plastics'), 'Total Amount'].sum()
        filtered_df_pie_g = filtered_df_pie[~filtered_df_pie['Product Category'].str.contains('Non-Plastics')]
        grouped_row = pd.DataFrame({'Product Category': ['Non-Plastics'], 'Percentage': [green_percentage], 'Total Amount': [green_amount]})
        filtered_df_pie_g = pd.concat([filtered_df_pie_g, grouped_row], ignore_index=True)

        # Assign colors based on category
        colors = ['green' if category == 'Non-Plastics' else 'red' for category in filtered_df_pie_g['Product Category']]

        # Modify labels
        labels = ['Plastics' if category == 'Single-Use Plastics' else 'Non-Plastics' for category in filtered_df_pie_g['Product Category']]

        # Create a pie chart with custom colors and labels
        fig, ax = plt.subplots()
        ax.pie(filtered_df_pie_g['Percentage'], labels=labels, autopct='%1.1f%%', colors=colors)

        # Add title
        ax.set_title('Percentage van de Plastics en Non-Plastics Totaalhoeveelheden')

        # Equal aspect ratio ensures that pie is drawn as a circle
        ax.axis('equal')

        # Display the chart using Streamlit
        st.pyplot(fig)
    else:
        st.write("Er zijn geen recente formulier reacties gevonden voor deze gebruiker.")

