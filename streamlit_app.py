import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Sample user data, ideally you would fetch this from a database
users = {
    "usernames": {
        "johndoe": {
            "name": "John Doe",
            "password": stauth.Hasher(["123"]).generate()[0],  # Hashed password
            "email": "johndoe@example.com"
        }
    }
}

# Save user data to a YAML file (for demonstration purposes)
with open('config.yaml', 'w') as file:
    yaml.dump(users, file)

# Load user data from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['usernames'],
    'some_cookie_name',
    'some_signature_key',
    cookie_expiry_days=30
)

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
    if new_username in users['usernames']:
        st.sidebar.error('Username already exists')
    else:
        hashed_password = stauth.Hasher([new_password]).generate()[0]
        users['usernames'][new_username] = {
            'name': new_name,
            'email': new_email,
            'password': hashed_password  # Store hashed password
        }
        with open('config.yaml', 'w') as file:
            yaml.dump(users, file)
        st.sidebar.success('User registered successfully')
        st.sidebar.info('Please refresh the page and log in')
