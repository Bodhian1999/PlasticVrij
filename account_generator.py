import random
from utils import create_user_account

# Define the number of user accounts to generate
num_accounts = 100

# Generate random usernames, emails, and passwords
usernames = [f"user{i+1}" for i in range(num_accounts)]
emails = [f"user{i+1}@example.com" for i in range(num_accounts)]
passwords = ["".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=8)) for _ in range(num_accounts)]

# Create user accounts
for username, email, password in zip(usernames, emails, passwords):
    create_user_account(username, email, password)

print(f"{num_accounts} accounts created successfully!")
