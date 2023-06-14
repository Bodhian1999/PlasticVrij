import hashlib
import os
import psycopg2
from configparser import ConfigParser
from decimal import Decimal

# Read the configuration file
config = ConfigParser()
config.read("config.ini")

def create_user_account(username, email, password, postal_code, company_name):
    conn = psycopg2.connect(
        host=config.get("postgresql", "host"),
        port=config.get("postgresql", "port"),
        database=config.get("postgresql", "database"),
        user=config.get("postgresql", "user"),
        password=config.get("postgresql", "password")
    )
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
    conn = psycopg2.connect(
        host=config.get("postgresql", "host"),
        port=config.get("postgresql", "port"),
        database=config.get("postgresql", "database"),
        user=config.get("postgresql", "user"),
        password=config.get("postgresql", "password")
    )
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
    conn = psycopg2.connect(
        host=config.get("postgresql", "host"),
        port=config.get("postgresql", "port"),
        database=config.get("postgresql", "database"),
        user=config.get("postgresql", "user"),
        password=config.get("postgresql", "password")
    )
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
    conn = psycopg2.connect(
        host=config.get("postgresql", "host"),
        port=config.get("postgresql", "port"),
        database=config.get("postgresql", "database"),
        user=config.get("postgresql", "user"),
        password=config.get("postgresql", "password")
    )
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