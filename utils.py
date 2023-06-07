import hashlib
import csv
import os

def create_users_file():
    if not os.path.isfile('users.csv') or os.stat('users.csv').st_size == 0:
        with open('users.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Email", "Password"])

def create_user_account(username, email, password):
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, email, hash_password(password)])

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(email, password):
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == email and row[2] == hash_password(password):
                return True
        return False

def get_user_email(username):
    with open('users.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return row[1]
    return None
