import streamlit as st
from view.login import login
from view.chat_room import chat_rooms
from view.admin_panel import admin_panel
from view.registration import registration

def main():
    st.title("Company Chat Application")

    menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Chat Rooms", "Admin Panel"])

    if menu == "Register":
        registration()

    elif menu == "Login":
        login()

    elif menu == "Chat Rooms":
        chat_rooms()

    elif menu == "Admin Panel":
        admin_panel()

if __name__ == "__main__":
    main()
