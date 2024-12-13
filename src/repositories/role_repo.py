from services.db import execute_query


def assign_role_to_employee(employee_id, role_id):
    """Assigns a role to an employee."""
    query = "INSERT INTO employee_roles (employee_id, role_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    execute_query(query, (employee_id, role_id))

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