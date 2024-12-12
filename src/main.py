import bcrypt
import psycopg2
import streamlit as st
from settings import DB_CONFIG

def execute_query(query: str, params=None):
    """Executes a query on the database."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if not query.strip().upper().startswith("SELECT") or query.split()[-2].upper() == "RETURNING":
                    conn.commit()
                return cursor.fetchall()
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

def authenticate_user(email, password):
    """Authenticate user using email and password."""
    query = """
    SELECT id, name, password_hash, EXISTS(
        SELECT 1 FROM employee_roles WHERE employee_id = employees.id AND role_id = (
            SELECT id FROM roles WHERE name = 'admin')) AS is_admin 
    FROM employees WHERE email = %s
    """
    result = execute_query(query, (email,))
    if result:
        user_id, name, password_hash, is_admin = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return {"id": user_id, "name": name, "is_admin": is_admin}
    return None

def register_user(name, email, password):
    """Registers a new user."""
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query = "INSERT INTO employees (name, email, password_hash) VALUES (%s, %s, %s)"
    return execute_query(query, (name, email, password_hash))

def list_user_chat_rooms(user_id):
    """Lists chat rooms where the user has messages."""
    query = """
    SELECT DISTINCT cr.id, cr.name, cr.description
    FROM chat_rooms cr
    JOIN messages m ON cr.id = m.chat_room_id
    WHERE m.employee_id = %s
    """
    return execute_query(query, (user_id,))

def create_chat_room(name, description, created_by):
    """Creates a new chat room and adds the creator as a participant."""
    query = "INSERT INTO chat_rooms (name, description) VALUES (%s, %s) RETURNING id"
    room_id_result = execute_query(query, (name, description))
    print(room_id_result, flush=True)
    if room_id_result:
        room_id = room_id_result[0][0]
        add_user_to_chat(created_by, room_id)
        return room_id
    return None

def send_message(employee_id, chat_room_id, content):
    """Sends a message to a chat room."""
    query = "INSERT INTO messages (content, employee_id, chat_room_id) VALUES (%s, %s, %s)"
    execute_query(query, (content, employee_id, chat_room_id))

def get_messages(chat_room_id):
    """Fetches messages for a chat room."""
    query = """
    SELECT messages.content, employees.name, messages.sent_at
    FROM messages
    JOIN employees ON messages.employee_id = employees.id
    WHERE chat_room_id = %s
    ORDER BY messages.sent_at ASC
    """
    return execute_query(query, (chat_room_id,))

def assign_role_to_employee(employee_id, role_name):
    """Assigns a role to an employee."""
    role_id_query = "SELECT id FROM roles WHERE name = %s"
    role_id = execute_query(role_id_query, (role_name,))
    if role_id:
        query = "INSERT INTO employee_roles (employee_id, role_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        execute_query(query, (employee_id, role_id[0][0]))

def assign_project_to_employee(employee_id, project_name):
    """Assigns a project to an employee."""
    project_id_query = "SELECT id FROM projects WHERE name = %s"
    project_id = execute_query(project_id_query, (project_name,))
    if project_id:
        query = "INSERT INTO employee_projects (employee_id, project_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        execute_query(query, (employee_id, project_id[0][0]))

def add_user_to_chat(employee_id, chat_room_id):
    """Adds a user to a chat room and logs a system message."""
    system_message = f"User {employee_id} joined the chat."
    send_message(employee_id, chat_room_id, system_message)

def main():
    st.title("Company Chat Application")

    menu = st.sidebar.selectbox("Menu", ["Login", "Register", "Chat Rooms", "Admin Panel"])

    if menu == "Register":
        st.subheader("Register")
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            if name and email and password:
                register_user(name, email, password)
                st.success("Registration successful. You can now log in.")
            else:
                st.error("All fields are required.")

    elif menu == "Login":
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

    elif menu == "Chat Rooms":
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
                    st.text(f"[{msg[2]}] {msg[1]}: {msg[0]}")

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
                    new_user_id = st.number_input("Enter User ID", min_value=1, step=1)
                    if st.button("Add User", key=f"add_user_{chat_room_id}"):
                        add_user_to_chat(new_user_id, chat_room_id)
                        st.success("User added to chat.")

        # Create a new chat room
        if st.checkbox("Create New Chat Room"):
            new_chat_name = st.text_input("Chat Room Name")
            new_chat_description = st.text_input("Description")
            if st.button("Create Chat"):
                create_chat_room(new_chat_name, new_chat_description, user['id'])
                st.success("Chat room created.")
                st.rerun()  # Refresh to show the new chat room



    elif menu == "Admin Panel":
        if "user" not in st.session_state or not st.session_state["user"]["is_admin"]:
            st.warning("Admin access required.")
            return

        st.subheader("Admin Panel")

        action = st.selectbox("Action", ["Assign Role", "Assign Project"])

        if action == "Assign Role":
            employee_id = st.number_input("Employee ID", min_value=1, step=1)
            role_name = st.text_input("Role Name")

            if st.button("Assign Role"):
                assign_role_to_employee(employee_id, role_name)
                st.success("Role assigned successfully.")

        elif action == "Assign Project":
            employee_id = st.number_input("Employee ID", min_value=1, step=1)
            project_name = st.text_input("Project Name")

            if st.button("Assign Project"):
                assign_project_to_employee(employee_id, project_name)
                st.success("Project assigned successfully.")

if __name__ == "__main__":
    main()
