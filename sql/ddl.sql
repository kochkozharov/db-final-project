-- Сотрудники
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    password_hash VARCHAR(128) NOT NULL
);

-- Комнаты чатов
CREATE TABLE chat_rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Сообщения
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    employee_id INT REFERENCES employees(id) ON DELETE CASCADE,
    chat_room_id INT REFERENCES chat_rooms(id) ON DELETE CASCADE
);

-- Роли
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Сотрудники и роли (многие ко многим)
CREATE TABLE employee_roles (
    employee_id INT REFERENCES employees(id) ON DELETE CASCADE,
    role_id INT REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (employee_id, role_id)
);

-- Проекты
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Сотрудники и проекты (многие ко многим)
CREATE TABLE employee_projects (
    employee_id INT REFERENCES employees(id) ON DELETE CASCADE,
    project_id INT REFERENCES projects(id) ON DELETE CASCADE,
    PRIMARY KEY (employee_id, project_id)
);
