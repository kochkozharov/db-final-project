import streamlit as st
from repositories.user_repo import authenticate_user
from settings import redis_client
import uuid
import json

def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            # 1. Генерируем уникальный токен
            token = str(uuid.uuid4())
            # 2. Подготовим данные для хранения
            data = json.dumps(user)
            # 3. Пишем в Redis с TTL
            redis_client.setex(f"auth:token:{token}", 600, data)
            # 4. Сохраняем токен в session_state
            st.session_state["auth_token"] = token

            st.success(f"Welcome, {user['name']}!")
        else:
            st.error("Invalid email or password.")