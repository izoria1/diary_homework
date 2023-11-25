import json

def load_accounts():
    try:
        with open('accounts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_accounts(accounts):
    with open('accounts.json', 'w') as file:
        json.dump(accounts, file)

def register_user(accounts):
    username = input("Enter new username: ")
    if username in accounts:
        print("Username already exists.")
        return False
    password = input("Enter new password: ")
    accounts[username] = password
    save_accounts(accounts)
    print("Registration successful.")
    return True

def login_user(accounts, username, password):
    return username in accounts and accounts[username] == password

