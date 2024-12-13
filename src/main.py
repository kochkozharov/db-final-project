import bcrypt
import psycopg2
import streamlit as st
from settings import DB_CONFIG

def execute_query(query: str, params=None):
    """Executes a query on the database."""
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT") or query.split()[-2].upper() == "RETURNING":
                return cursor.fetchall()
            conn.commit()
            return

def get_user_name_by_id(user_id):
    """Fetches the name of the user by their ID."""
    query = "SELECT name FROM employees WHERE id = %s"
    result = execute_query(query, (user_id,))
    if result:
        return result[0][0]
    return None

def get_user_id_by_email(email):
    """Fetches the user ID by their email."""
    query = "SELECT id FROM employees WHERE email = %s"
    result = execute_query(query, (email,))
    if result:
        return result[0][0]
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
    """Fetches messages for a chat room with additional user info."""
    query = """
    SELECT 
        messages.content, 
        employees.name, 
        TO_CHAR(messages.sent_at, 'HH24:MI') AS sent_time,
        COALESCE(array_to_string(array(
            SELECT r.name FROM roles r
            JOIN employee_roles er ON r.id = er.role_id
            WHERE er.employee_id = employees.id
        ), ', '), 'No Role') AS roles,
        COALESCE(array_to_string(array(
            SELECT p.name FROM projects p
            JOIN employee_projects ep ON p.id = ep.project_id
            WHERE ep.employee_id = employees.id
        ), ', '), 'No Project') AS projects
    FROM messages
    JOIN employees ON messages.employee_id = employees.id
    WHERE chat_room_id = %s
    ORDER BY messages.sent_at ASC
    """
    return execute_query(query, (chat_room_id,))

def get_id_by_role_name(role_name):
    role_id_query = "SELECT id FROM roles WHERE name = %s"
    role_id = execute_query(role_id_query, (role_name,))
    return role_id[0][0] if role_id else None

def get_id_by_project_name(project_name):
    project_id_query = "SELECT id FROM projects WHERE name = %s"
    project_id = execute_query(project_id_query, (project_name,))
    return project_id[0][0] if project_id else None

def assign_role_to_employee(employee_id, role_id):
    """Assigns a role to an employee."""
    query = "INSERT INTO employee_roles (employee_id, role_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    execute_query(query, (employee_id, role_id))

def assign_project_to_employee(employee_id, project_id):
    query = "INSERT INTO employee_projects (employee_id, project_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    execute_query(query, (employee_id, project_id))

def add_user_to_chat(employee_id, chat_room_id):
    """Adds a user to a chat room and logs a system message."""
    system_message = f"User {get_user_name_by_id(employee_id)} joined the chat."
    send_message(employee_id, chat_room_id, system_message)

def add_role(role_name):
    """Adds a new role."""
    query = "INSERT INTO roles (name) VALUES (%s) RETURNING id"
    result = execute_query(query, (role_name,))
    if result:
        return result[0][0]
    return None

def delete_role(role_name):
    """Deletes a role by name."""
    query = "DELETE FROM roles WHERE name = %s"
    result = execute_query(query, (role_name,))
    if result is not None:
        return True  # Возвращаем True, если запрос выполнен успешно
    else:
        return False  # Если запрос не выполнен, возвращаем False

def add_project(project_name):
    """Adds a new project."""
    query = "INSERT INTO projects (name) VALUES (%s) RETURNING id"
    result = execute_query(query, (project_name,))
    if result:
        return result[0][0]
    return None

def delete_project(project_name):
    """Deletes a project by name."""
    query = "DELETE FROM projects WHERE name = %s"
    result = execute_query(query, (project_name,))
    if result is not None:
        return True  # Возвращаем True, если запрос выполнен успешно
    else:
        return False  # Если запрос не выполнен, возвращаем False


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
                try:
                    register_user(name, email, password)
                except:
                    st.error("Email already used.")
                else:
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

        action = st.selectbox("Action", ["Assign Role", "Assign Project", "Add Role", "Add project", "Delete Role", "Delete project"])

        # Capture employee_id after email input, common for both actions

                # Proceed with actions if user exists
        if action == "Assign Role":
            email = st.text_input("Email")
            if email:
                employee_id = get_user_id_by_email(email)
                if not employee_id:
                    st.error("No such user.")
                else:
                    role_name = st.text_input("Role Name")
                    if role_name:
                        role_id = get_id_by_role_name(role_name)
                        if not role_id:
                            st.error("No such role.")
                        elif st.button("Assign Role"):
                            assign_role_to_employee(employee_id, role_id)
                            st.success("Role assigned successfully.")

        elif action == "Assign Project":
            email = st.text_input("Email")
            if email:
                employee_id = get_user_id_by_email(email)
                if not employee_id:
                    st.error("No such user.")
                else:
                    project_name = st.text_input("Project Name")
                    if project_name:
                        project_id = get_id_by_project_name(project_name)
                        if not project_id:
                            st.error("No such project.")
                        elif st.button("Assign Project"):
                            assign_project_to_employee(employee_id, project_id)
                            st.success("Project assigned successfully.")

        elif action == "Add Role":
            new_role_name = st.text_input("New Role Name")
            if new_role_name:
                if st.button("Add Role"):
                    role_id = add_role(new_role_name)
                    if role_id:
                        st.success(f"Role '{new_role_name}' added successfully.")
                    else:
                        st.error("Failed to add role.")

        elif action == "Delete Role":
            role_name_to_delete = st.text_input("Role Name to Delete")
            if role_name_to_delete:
                if st.button("Delete Role"):
                    success = delete_role(role_name_to_delete)
                    if success:
                        st.success(f"Role '{role_name_to_delete}' deleted successfully.")
                    else:
                        st.error(f"Role '{role_name_to_delete}' does not exist.")

        elif action == "Add project":
            new_project_name = st.text_input("New project Name")
            if new_project_name:
                if st.button("Add project"):
                    project_id = add_project(new_project_name)

        elif action == "Delete project":
            project_name_to_delete = st.text_input("project Name to Delete")
            if project_name_to_delete:
                if st.button("Delete project"):
                    success = delete_project(project_name_to_delete)





if __name__ == "__main__":
    main()
