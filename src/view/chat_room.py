import streamlit as st
from repositories.chat_repo import get_messages, add_user_to_chat, create_chat_room
from repositories.user_repo import list_user_chat_rooms, send_message
from services.mappers import get_user_id_by_email

def chat_rooms():
    if "user" not in st.session_state:
        st.warning("Please log in first.")
        return

    user = st.session_state["user"]

    st.subheader("Chat Rooms")

    # Fetch chat rooms
    chat_rooms = list_user_chat_rooms(user["id"])
    if chat_rooms:
        chat_room = st.selectbox("Select Chat Room", chat_rooms, format_func=lambda x: x[1])
        if chat_room:
            chat_room_id = chat_room[0]
            st.subheader(f"Chat Room: {chat_room[1]}")

            # Display messages
            messages = get_messages(chat_room_id)
            for msg in messages:
                content, sender_name, sent_time, roles, projects = msg
                st.text(f"[{sent_time}] {sender_name} ({roles}; {projects}): {content}")

            # Input for new message
            if f"message_{chat_room_id}" not in st.session_state:
                st.session_state[f"message_{chat_room_id}"] = ""

            new_message = st.text_input(
                "Your message",
                value=st.session_state[f"message_{chat_room_id}"],
                key=f"input_message_{chat_room_id}"
            )

            if st.button("Send", key=f"send_{chat_room_id}"):
                if new_message.strip():
                    send_message(user['id'], chat_room_id, new_message)
                    st.session_state[f"message_{chat_room_id}"] = ""  # Clear the input field
                    st.rerun()  # Refresh the page to show the new message

            # Add a new user to the chat
            if st.checkbox("Add a new user to this chat"):
                new_user_email = st.text_input("Email")
                new_user_id = get_user_id_by_email(new_user_email)
                if new_user_email:
                    if st.button("Add User", key=f"add_user_{chat_room_id}"):
                        add_user_to_chat(new_user_id, chat_room_id)
                        st.success("User added to chat.")
                else:
                    st.error("No such user.")

    # Create a new chat room
    if st.checkbox("Create New Chat Room"):
        new_chat_name = st.text_input("Chat Room Name")
        new_chat_description = st.text_input("Description")
        if st.button("Create Chat"):
            create_chat_room(new_chat_name, new_chat_description, user['id'])
            st.success("Chat room created.")
            st.rerun()  # Refresh to show the new chat room