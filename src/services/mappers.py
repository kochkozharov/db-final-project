from services.db import execute_query

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

def get_id_by_role_name(role_name):
    role_id_query = "SELECT id FROM roles WHERE name = %s"
    role_id = execute_query(role_id_query, (role_name,))
    return role_id[0][0] if role_id else None

def get_id_by_project_name(project_name):
    project_id_query = "SELECT id FROM projects WHERE name = %s"
    project_id = execute_query(project_id_query, (project_name,))
    return project_id[0][0] if project_id else None