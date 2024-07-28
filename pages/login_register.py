
import streamlit as st

def show_login_register(user_data, hash_password, save_user_data):
    st.sidebar.title("Login / Register")
    choice = st.sidebar.selectbox("Choose Action", ["Login", "Register"])

    if choice == "Login":
        st.sidebar.subheader("Login")
        login_username = st.sidebar.text_input("Username")
        login_password = st.sidebar.text_input("Password", type="password")
        login_button = st.sidebar.button("Login")
        
        if login_button:
            hashed_input_password = hash_password(login_password)
            if login_username in user_data and user_data[login_username] == hashed_input_password:
                st.sidebar.success("Logged in successfully!")
                st.session_state.logged_in = True
                st.session_state.username = login_username
                st.session_state.page = 'Home'
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
