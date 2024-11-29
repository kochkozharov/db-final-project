import bcrypt


# Хеширование пароля
def hash_password(password):
    salt = bcrypt.gensalt()  # Генерация соли
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


# Проверка пароля
def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


# Пример
password = "my_secure_password"
hashed = hash_password(password)
print(f"Хешированный пароль: {hashed}")

is_valid = check_password("my_secure_password", hashed)
print(f"Пароль валиден: {is_valid}")
