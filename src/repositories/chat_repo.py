from services.db import execute_query
from services.mappers import get_user_name_by_id
from repositories.user_repo import send_message
from settings import redis_client
import json

def create_chat_room(name, description, created_by):
    """Creates a new chat room and adds the creator as a participant."""
    query = "INSERT INTO chat_rooms (name, description) VALUES (%s, %s) RETURNING id"
    room_id_result = execute_query(query, (name, description))
    if room_id_result:
        room_id = room_id_result[0][0]
        add_user_to_chat(created_by, room_id)
        return room_id
    return None

def get_messages(chat_room_id):
    """Fetches messages for a chat room with additional user info."""
    cache_key = f"chat_messages:{chat_room_id}"
    
    # 1. Попробовать получить из Redis
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
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
    rows = execute_query(query, (chat_room_id,))
    redis_client.setex(cache_key, 60, json.dumps(rows))
    return rows

def delete_chat(chat_name):
    """Deletes a chat by name."""
    # Check if the chat exists by name
    query = "SELECT id FROM chat_rooms WHERE name = %s"
    result = execute_query(query, (chat_name,))
    
    if result:
        chat_id = result[0][0]
        # Delete the chat
        query = "DELETE FROM chat_rooms WHERE name = %s"
        execute_query(query, (chat_name,))
        return True
    else:
        return False

def add_user_to_chat(employee_id, chat_room_id):
    """Adds a user to a chat room and logs a system message."""
    system_message = f"User {get_user_name_by_id(employee_id)} joined the chat."
    send_message(employee_id, chat_room_id, system_message)
    cache_key = f"user:{employee_id}:chat_rooms"
    redis_client.delete(cache_key)
