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

    sql = f"INSERT INTO form_responses ({columns}) VALUES ({placeholders})"
    cursor.execute(sql, values)

    conn.commit()
    cursor.close()
    conn.close()
    
def get_user_score(email, non_plastics_percentage):
    # Create a database connection
    conn = create_connection()
    cursor = conn.cursor()

    # Query the database to get the user's form responses
    cursor.execute("SELECT * FROM form_responses WHERE Email = %s", (email,))
    user_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if user_data:
        # Extract the form response data from the query result
        ja_count = user_data[1]
        nee_count = user_data[2]
        total_count = user_data[3]
        avg_score_total = user_data[4]
        count_total = user_data[5]

        # Calculate the user's score based on the form responses
        if total_count > 0:
            user_score = (ja_count / total_count) * 100
            avg_score = avg_score_total / count_total
        else:
            user_score = 0
            avg_score = 0

        # Adjust user score based on non-plastics percentage
        non_plastics_score = non_plastics_percentage * 10
        user_score_adjusted = max(user_score, non_plastics_score)

        return user_score_adjusted, avg_score
    else:
        return None, None
