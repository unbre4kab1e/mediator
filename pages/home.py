import streamlit as st

def show_home():
    st.write(f"Welcome, {st.session_state.username}!")
    st.title("Fill a Ticket")
    
    with st.form("ticket_form"):
        email = st.text_input("Enter the email of the person you are filling the ticket against:")
        ticket_details = st.text_area("Enter ticket details:")
        submit = st.form_submit_button("Submit")
        
        if submit:
            st.success(f"Ticket submitted for {email}")
