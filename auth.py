import json
import os
import bcrypt

USER_FILE = "fitness_data/users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    os.makedirs(os.path.dirname(USER_FILE), exist_ok=True)
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(email, password):
    users = load_users()
    if email in users:
        return False, "User already exists."
    
    users[email] = {
        "password": hash_password(password)
    }
    save_users(users)
    return True, "Registration successful."

def login_user(email, password):
    users = load_users()
    if email not in users:
        return False, "Invalid email or password."
    
    if verify_password(password, users[email]["password"]):
        return True, "Login successful."
    return False, "Invalid email or password."
