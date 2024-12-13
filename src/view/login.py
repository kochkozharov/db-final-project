import streamlit as st
from repositories.user_repo import authenticate_user

def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state["user"] = user
            st.success(f"Welcome, {user['name']}!")
        else:
            st.error("Invalid email or password.")