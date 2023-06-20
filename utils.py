import hashlib
import os
import psycopg2
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

def get_recent_form_response(email):
    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    # Query the database to get the most recent form response for the email
    cursor.execute("""
        SELECT *
        FROM form_responses_n
        WHERE email = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (email,))
    
    # Fetch the row
    recent_response = cursor.fetchone()

    cursor.close()
    conn.close()

    return recent_response

def calculate_non_plastics_percentage(recent_response):
    if recent_response:
        # Calculate the percentage of 'Non-Plastics' in the form response
        non_plastics_count = sum(
            field == 'Non-Plastics'
            for field in recent_response[2:-50]  # Exclude 'id' and 'email' fields from count
        )
        total_count = len(recent_response[2:-50])  # Exclude 'id' and 'email' fields from count

        non_plastics_percentage = non_plastics_count / total_count

        return non_plastics_percentage
    else:
        return None


def calculate_non_plastics_percentage(email):
    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    # Query the database to get the user's form responses
    cursor.execute("SELECT * FROM form_responses_n WHERE email = %s", (email,))
    data = cursor.fetchone()

    cursor.close()
    conn.close()

    if data:
        # Calculate the percentage of 'Non-Plastics' in the form responses
        non_plastics_count = sum(
            field == 'Non-Plastics'
            for field in data[2:-50]  # Exclude 'id' and 'email' fields from count
        )
        total_count = len(data[2:-50])  # Exclude 'id' and 'email' fields from count

        non_plastics_percentage = non_plastics_count / total_count

        return non_plastics_percentage
    else:
        return None


def get_user_score(email, non_plastics_percentage):
    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    # Query the database to get the user's form responses
    cursor.execute("SELECT * FROM form_responses_n WHERE email = %s", (email,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        # Extract the form response data from the query result
        ja_counts = user_data[-48:-24]  # Get counts of 'ja' responses for each field
        total_counts = user_data[-24:]  # Get total counts for each field

        # Calculate the user's score based on the form responses
        if any(total_counts):
            user_score = (sum(ja_counts) / sum(total_counts)) * 10
            avg_score = sum(user_data[-24:]) / sum(total_counts)
        else:
            user_score = 0
            avg_score = 0

        # Adjust user score based on non-plastics percentage
        non_plastics_score = non_plastics_percentage * 10
        user_score_adjusted = max(user_score, non_plastics_score)

        return user_score_adjusted, avg_score
    else:
        return None, None
