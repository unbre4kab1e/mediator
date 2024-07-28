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

# Function to check password strength
def check_password_strength(password):
    if len(password) < 6:
        return False
    return True

# Load user data
user_data = load_user_data()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# User login/registration
if not st.session_state.logged_in:
    st.title("Login / Register")

    choice = st.selectbox("Choose Action", ["Login", "Register"], index=0 if not st.session_state.show_register else 1)

    if choice == "Login":
        st.subheader("Login")
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        
        if login_button:
            hashed_input_password = hash_password(login_password)
            if login_username in user_data and user_data[login_username]["password"] == hashed_input_password:
                st.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.username = user_data[login_username]["name"]
                st.experimental_rerun()  # Refresh the page to hide the login form
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        st.subheader("Register")
        reg_name = st.text_input("Full name")
        reg_age = st.text_input("Age")
        reg_gender = st.selectbox("Choose Gender", ["Male", "Female"])
        reg_username = st.text_input("Username")
        reg_password = st.text_input("Password", type="password")
        reg_confirm_password = st.text_input("Confirm Password", type="password")
        reg_button = st.button("Register")
        
        if reg_button:
            if reg_username in user_data:
                st.error("Username already exists")
            elif not check_password_strength(reg_password):
                st.error("Password must be at least 6 characters long")
            elif reg_password != reg_confirm_password:
                st.error("Passwords do not match")
            else:
                user_data[reg_username] = {
                    'password': hash_password(reg_password),
                    'name': reg_name,
                    'age': reg_age,
                    'gender': reg_gender
                }
                save_user_data(user_data)
                st.success("User registered successfully")
                st.session_state.show_register = False
                st.experimental_rerun()  # Refresh the page to show the login form after registration

    if choice == "Register" and st.session_state.show_register is False:
        st.session_state.show_register = True
        st.experimental_rerun()

else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()  # Refresh the page to show the login form after logout

# Main app
if st.session_state.logged_in:
    st.write(f"Welcome, {st.session_state.username}!")
    st.title("Fill a Ticket")
    
    with st.form("ticket_form"):
        email = st.text_input("Enter the email of the person you are filling the ticket against:")
        ticket_details = st.text_area("Enter ticket details:")
        submit = st.form_submit_button("Submit")
        
        if submit:
            st.success(f"Ticket submitted for {email}")
