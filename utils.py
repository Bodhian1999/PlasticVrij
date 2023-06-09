import hashlib
import os
import psycopg2
import pandas as pd
import datetime
from configparser import ConfigParser
from decimal import Decimal

def create_connection():
    # Read the database configuration from a file
    config = ConfigParser()
    config.read("config.ini")

    # Create a connection to the database
    conn = psycopg2.connect(
        host=config.get("postgresql", "host"),
        port=config.get("postgresql", "port"),
        database=config.get("postgresql", "database"),
        user=config.get("postgresql", "user"),
        password=config.get("postgresql", "password")
    )

    return conn

def create_user_account(username, email, password, postal_code, company_name):
    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "INSERT INTO users (username, email, password, postal_code, company_name) VALUES (%s, %s, %s, %s, %s)",
        (username, email, hashed_password, postal_code, company_name)
    )

    conn.commit()
    cursor.close()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(email, password):
    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE email = %s AND password = %s",
        (email, hashed_password)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return True
    else:
        return False

def get_user_email(username):
    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM users WHERE username = %s",
        (username,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    else:
        return None
    

def insert_form_responses(responses):

    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    placeholders = ', '.join(['%s'] * len(responses))
    columns = ', '.join(responses.keys())
    values = list(responses.values())

    # Convert the relevant values to Decimal type
    for i, value in enumerate(values):
        if isinstance(value, int):
            values[i] = Decimal(value)

    sql = f"INSERT INTO form_responses_n ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()
    
def get_all_form_responses(current_user_email):
    # Retrieve all form responses for the current user email
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM form_responses_n WHERE email = %s ORDER BY created_at DESC"
    cursor.execute(query, (current_user_email,))
    responses = cursor.fetchall()

    cursor.close()
    conn.close()

    if responses:
        # Convert the responses to a dataframe
        columns = [column[0] for column in cursor.description]
        response_data = [dict(zip(columns, response)) for response in responses]
        response_df = pd.DataFrame(response_data)
        return response_df
    else:
        return None

def get_recent_form_response(current_user_email):
    # Retrieve the recent form response for the current user email
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM form_responses_n WHERE email = %s ORDER BY created_at DESC LIMIT 1"
    cursor.execute(query, (current_user_email,))
    response = cursor.fetchone()

    cursor.close()
    conn.close()

    if response:
        # Convert the response tuple to a dictionary
        columns = [column[0] for column in cursor.description]
        response_dict = dict(zip(columns, response))
        # Create a DataFrame from the response dictionary
        df = pd.DataFrame(response_dict, index=[0])
        return df
    else:
        return None
    
def get_recent_form_responses():
    # Retrieve the most recent form response for each unique user email
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT DISTINCT ON (email) * FROM form_responses_n ORDER BY email, created_at DESC"
    cursor.execute(query)
    responses = cursor.fetchall()

    cursor.close()
    conn.close()

    if responses:
        # Convert the responses to a dataframe
        columns = [column[0] for column in cursor.description]
        response_data = [dict(zip(columns, response)) for response in responses]
        response_df = pd.DataFrame(response_data)
        return response_df
    else:
        return None


import math

def calculate_non_plastics_percentage(recent_response):
    total_items = 0
    non_plastic_items = 0

    # Loop over the categories and calculate the percentage
    categories = [
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
        'natte_doekjes_garnalen_spareribs'
    ]

    for category in categories:
        product_category = recent_response['product_category_' + category]
        if (
            product_category != 'Single-Use Plastics' and
            product_category != 'n.v.t. (product uit assortiment gehaald)'
        ):
            # Convert NaN values to 0
            if math.isnan(recent_response.get('aantal_' + category)):
                recent_response['aantal_' + category] = 0
            non_plastic_items += int(recent_response['aantal_' + category])
            total_items += int(recent_response['aantal_' + category])

    # Calculate the percentage
    if total_items > 0:
        non_plastic_percentage = (non_plastic_items / total_items) * 100
    else:
        non_plastic_percentage = 0

    return non_plastic_percentage


def calculate_sustainability_score(user_percentage):
    score_range = 10  # Set the desired score range
    score = (user_percentage / 100) * score_range
    return score if score <= score_range else score_range

    
def calculate_sustainability_percentage(selected_row):
    total_count = 0
    single_use_plastics_count = 0
    sustainable_count = 0 
    
    for column in selected_row:
        total_count += 1
        value = selected_row[column].values[0]
        if value == "Single-Use Plastics":
            single_use_plastics_count += 1
        else:
            sustainable_count += 1

    sustainability_percentage = (sustainable_count / total_count) * 100

    return sustainability_percentage


def calculate_avg_sustainability_percentage(df):
    total_percentage = 0
    for index, row in df.iterrows():
        selected_row = pd.DataFrame(row[row.index[22:41]]).T
        sustainability_percentage = calculate_sustainability_percentage(selected_row)
        
        total_percentage += sustainability_percentage
    
    average_percentage = total_percentage / len(df)
    return average_percentage

def insert_avg_sustainability_score(avg_sustainability_score):
    conn = create_connection()
    cursor = conn.cursor()

    current_date = datetime.datetime.now()  # Get the current date and time

    query = "INSERT INTO avg_sus_score (date, avg_sustainability_score) VALUES (%s, %s)"
    values = (current_date, avg_sustainability_score)
    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()

def get_latest_avg_sustainability_score():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT avg_sustainability_score FROM avg_sus_score ORDER BY date DESC LIMIT 1")
    result = cursor.fetchone()
    latest_avg_sustainability_score = result[0] if result else None

    cursor.close()
    conn.close()

    return latest_avg_sustainability_score

def get_avg_sustainability_scores():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM avg_sus_score ORDER BY date")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    if rows:
        df = pd.DataFrame(rows, columns=columns)
        return df
    else:
        return pd.DataFrame()

def get_all_user_data():
    # Retrieve all data from "users"
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users"
    cursor.execute(query)
    user_data = cursor.fetchall()

    cursor.close()
    conn.close()

    if user_data:
        # Convert the data to a dataframe
        columns = [column[0] for column in cursor.description]
        user_data = [dict(zip(columns, data)) for data in user_data]
        user_df = pd.DataFrame(user_data)
        return user_df
    else:
        return None
