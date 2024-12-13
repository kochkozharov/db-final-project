import streamlit as st
from repositories.user_repo import register_user

def registration():
    st.subheader("Register")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if name and email and password:
            try:
                register_user(name, email, password)
            except:
                st.error("Email already used.")
            else:
                st.success("Registration successful. You can now log in.")
        else:
            st.error("All fields are required.")