import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from pathlib import Path

# Define a function to load the user data from the YAML file
def load_user_data():
    config_path = Path('config.yaml')
    if config_path.exists():
        with open(config_path, 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)
            if config is None:
                config = {"usernames": {}}
            return config
    else:
        return {"usernames": {}}

# Define a function to save the user data to the YAML file
def save_user_data(config):
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file)

# Load the user data
config = load_user_data()

# Ensure the 'usernames' key exists
if 'usernames' not in config:
    config['usernames'] = {}

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['usernames'],
    'some_cookie_name',
    'some_signature_key',
    cookie_expiry_days=30
)

# Authentication logic
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    st.write(f'Welcome *{name}*')
    st.title('Fill a Ticket')

    # Ticket Form
    with st.form("ticket_form"):
        email = st.text_input('Enter the email of the person you are filling the ticket against:')
        ticket_details = st.text_area('Enter ticket details:')
        submit = st.form_submit_button('Submit')

        if submit:
            st.success(f'Ticket submitted for {email}')
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')

# Registration
st.sidebar.title("Register")
new_username = st.sidebar.text_input('New username')
new_name = st.sidebar.text_input('New name')
new_email = st.sidebar.text_input('New email')
new_password = st.sidebar.text_input('New password', type='password')
register = st.sidebar.button('Register')

if register:
    if new_username in config['usernames']:
        st.sidebar.error('Username already exists')
    else:
        hashed_password = stauth.Hasher([new_password]).generate()[0]
        config['usernames'][new_username] = {
            'name': new_name,
            'email': new_email,
            'password': hashed_password  # Store hashed password
        }
        save_user_data(config)
        st.sidebar.success('User registered successfully')
        st.sidebar.info('Please refresh the page and log in')
