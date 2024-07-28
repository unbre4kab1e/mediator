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

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = 'Login / Register'

# Import page modules
import pages.login_register as login_register
import pages.home as home

# Page Navigation
if st.session_state.logged_in:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Logout"])
    
    if page == "Home":
        st.session_state.page = 'Home'
    elif page == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.page = 'Login / Register'
else:
    st.session_state.page = 'Login / Register'

# Page Rendering
if st.session_state.page == 'Login / Register':
    login_register.show_login_register(user_data, hash_password, save_user_data)
elif st.session_state.page == 'Home':
    home.show_home()
