import datetime
from services.db import execute_query
import bcrypt
from settings import redis_client
import json
from services.mappers import get_user_id_by_email

def authenticate_user(email, password):
    """Authenticate user using email and password."""
    user_id = get_user_id_by_email(email)
    cache_key = f"user:auth:{user_id}"
    
    # 1) Попытаться взять данные из Redis
    cached = redis_client.get(cache_key)
    if cached:
        result = json.loads(cached)
    else:
        query = """
        SELECT id, name, password_hash, EXISTS(
            SELECT 1 FROM employee_roles WHERE employee_id = employees.id AND role_id = (
                SELECT id FROM roles WHERE name = 'admin')) AS is_admin 
        FROM employees WHERE email = %s
        """
        result = execute_query(query, (email,))
        redis_client.setex(cache_key, 600, json.dumps(result))
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
    key = f"user:{user_id}:chat_rooms"
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    """Lists chat rooms where the user has messages."""
    query = """
    SELECT DISTINCT cr.id, cr.name, cr.description
    FROM chat_rooms cr
    JOIN messages m ON cr.id = m.chat_room_id
    WHERE m.employee_id = %s
    """
    rooms = execute_query(query, (user_id,))
    redis_client.setex(key, 60, json.dumps(rooms))
    return rooms

def send_message(employee_id, chat_room_id, content):
    """Sends a message to a chat room."""
    cache_key = f"chat_messages:{chat_room_id}"
    redis_client.delete(cache_key)
    query = "INSERT INTO messages (content, employee_id, chat_room_id) VALUES (%s, %s, %s)"
    execute_query(query, (content, employee_id, chat_room_id))
    payload = {
        "type": "new_chat_message",
        "chat_room_id": chat_room_id,
        "sender_id": employee_id,
        "content": content,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    redis_client.publish(f"critical_events", json.dumps(payload))

def delete_user(email):
    """Deletes a user by email."""
    # Check if the user exists by email
    id = get_user_id_by_email(email)
    cache_key = f"user:auth:{id}"
    redis_client.delete(cache_key)
    cache_key = f"user:id_by_email:{email}"
    redis_client.delete(cache_key)

    query = "SELECT id FROM employees WHERE email = %s"
    result = execute_query(query, (email,))
    
    if result:
        user_id = result[0][0]
        # Delete the user
        query = "DELETE FROM employees WHERE email = %s"
        execute_query(query, (email,))
        return True
    else:
        return False