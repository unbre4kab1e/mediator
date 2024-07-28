import streamlit as st
import json
import hashlib
from pathlib import Path

# Path to the JSON file where user data is stored
USER_DATA_FILE = 'users.json'

# Function to load user data from JSON file
def load_user_data():
    if Path(USER_DATA_FILE).exists():
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    else:
        return {}

# Function to save user data to JSON file
def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(data, file)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load user data
user_data = load_user_data()

# Authentication status
logged_in = False
username = None

# User login/registration
st.sidebar.title("Login / Register")
choice = st.sidebar.selectbox("Choose Action", ["Login", "Register"])

if choice == "Login":
    st.sidebar.subheader("Login")
    login_username = st.sidebar.text_input("Username")
    login_password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")
    
    if login_button:
        if login_username in user_data and user_data[login_username] == hash_password(login_password):
            st.sidebar.success("Logged in successfully!")
            logged_in = True
            username = login_username
        else:
            st.sidebar.error("Invalid username or password")

elif choice == "Register":
    st.sidebar.subheader("Register")
    reg_username = st.sidebar.text_input("New Username")
    reg_password = st.sidebar.text_input("New Password", type="password")
    reg_button = st.sidebar.button("Register")
    
    if reg_button:
        if reg_username in user_data:
            st.sidebar.error("Username already exists")
        else:
            user_data[reg_username] = hash_password(reg_password)
            save_user_data(user_data)
            st.sidebar.success("User registered successfully")

# Main app
if logged_in:
    st.write(f"Welcome, {username}!")
    st.title("Fill a Ticket")
    
    with st.form("ticket_form"):
        email = st.text_input("Enter the email of the person you are filling the ticket against:")
        ticket_details = st.text_area("Enter ticket details:")
        submit = st.form_submit_button("Submit")
        
        if submit:
            st.success(f"Ticket submitted for {email}")
else:
    st.warning("Please log in to access this section.")
