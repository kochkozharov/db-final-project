-- Добавляем роли
INSERT INTO roles (name) VALUES 
('Developer'), 
('Manager'), 
('Tester');

-- Добавляем сотрудников
INSERT INTO employees (name, email, password_hash) VALUES 
('John Doe', 'john.doe@example.com', '1231'),
('Jane Smith', 'jane.smith@example.com', '1231'),
('Alice Johnson', 'alice.johnson@example.com', '1231');

-- Связываем сотрудников с ролями
INSERT INTO employee_roles (employee_id, role_id) VALUES
(1, 1), -- John Doe - Developer
(2, 2), -- Jane Smith - Manager
(3, 3); -- Alice Johnson - Tester

-- Добавляем проекты
INSERT INTO projects (name) VALUES 
('Banking App'),
('CRM System'),
('Data Analytics');

-- Связываем сотрудников с проектами
INSERT INTO employee_projects (employee_id, project_id) VALUES
(1, 1), -- John Doe - Banking App
(2, 2), -- Jane Smith - CRM System
(3, 3); -- Alice Johnson - Data Analytics

-- Добавляем комнаты чатов
INSERT INTO chat_rooms (name, description) VALUES 
('General Discussion', 'General chat room for all employees'),
('Project Updates', 'Chat room for project-related updates');

-- Добавляем сообщения
INSERT INTO messages (content, employee_id, chat_room_id) VALUES
('Hello everyone!', 1, 1), -- John Doe in General Discussion
('Project updates coming soon.', 2, 2), -- Jane Smith in Project Updates
('Testing completed.', 3, 2); -- Alice Johnson in Project Updates
