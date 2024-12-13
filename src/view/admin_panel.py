import streamlit as st

from services.mappers import get_user_id_by_email, get_id_by_role_name, get_id_by_project_name
from repositories.project_repo import assign_project_to_employee, add_project, delete_project
from repositories.role_repo import assign_role_to_employee, add_role, delete_role
from repositories.chat_repo import delete_chat
from repositories.user_repo import delete_user


def admin_panel():       
    if "user" not in st.session_state or not st.session_state["user"]["is_admin"]:
            st.warning("Admin access required.")
            return

    st.subheader("Admin Panel")

    action = st.selectbox("Action", ["Assign Role", "Assign Project", "Add Role", "Add project", "Delete Role", "Delete project", "Delete Chat", "Delete User"])

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
                try:
                    role_id = add_role(new_role_name)
                except:
                    st.error("Such role already exists.")
                else:
                    st.success(f"Role '{new_role_name}' added successfully.")

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
                try:
                    project_id = add_project(new_project_name)
                except:
                    st.error("Such project already exists.")
                else:
                    st.success(f"Project '{new_project_name}' added successfully.")

    elif action == "Delete project":
        project_name_to_delete = st.text_input("project Name to Delete")
        if project_name_to_delete:
            if st.button("Delete project"):
                success = delete_project(project_name_to_delete)

    elif action == "Delete Chat":
        chat_name = st.text_input("chat name to delete")
        if chat_name:
            if st.button("Delete Chat"):
                res = delete_chat(chat_name)
                if res:
                    st.success(f"Chat with name '{chat_name}' has been deleted.")
                else:
                    st.error(f"Chat with name '{chat_name}' not found.")
                    
    elif action == "Delete User":
        email = st.text_input("user's email to delete")
        if email:
            if st.button("Delete User"):
                res = delete_user(email)
                if res:
                    st.success(f"User with email '{email}' has been deleted.")
                else:
                    st.error(f"User with email '{email}' not found.")