from services.db import execute_query

def assign_project_to_employee(employee_id, project_id):
    query = "INSERT INTO employee_projects (employee_id, project_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    execute_query(query, (employee_id, project_id))

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