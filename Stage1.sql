-- =========================================================
-- Yuktishaalaa Stage 1
-- Employee Onboarding Tracker
-- Table Creation + Sample Data
-- =========================================================

-- =========================================================
-- 1. ROLES
-- =========================================================

CREATE TABLE roles (
    role_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (role_name)
VALUES
    ('HR'),
    ('Manager'),
    ('Employee');


-- =========================================================
-- 2. USERS
-- =========================================================

CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id BIGINT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_users_role
        FOREIGN KEY (role_id)
        REFERENCES roles(role_id)
);

INSERT INTO users
    (username, email, password_hash, role_id)
VALUES
    ('Priya HR', 'priya.hr@yuktishaalaa.com', 'demo_hash_hr', 1),
    ('Rahul Manager', 'rahul.manager@yuktishaalaa.com', 'demo_hash_manager', 2),
    ('Arjun Employee', 'arjun.employee@yuktishaalaa.com', 'demo_hash_employee', 3),
    ('Neha Employee', 'neha.employee@yuktishaalaa.com', 'demo_hash_employee', 3);


-- =========================================================
-- 3. EMPLOYEES
-- =========================================================

CREATE TABLE employees (
    employee_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_code VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100),
    email VARCHAR(255) NOT NULL UNIQUE,
    joining_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO employees
    (employee_code, first_name, last_name, email, joining_date)
VALUES
    ('EMP001', 'Arjun', 'Kumar',
     'arjun.employee@yuktishaalaa.com', '2026-10-01'),

    ('EMP002', 'Neha', 'Sharma',
     'neha.employee@yuktishaalaa.com', '2026-10-05');


-- =========================================================
-- 4. ONBOARDING
-- =========================================================

CREATE TABLE onboarding (
    onboarding_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id BIGINT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    started_date DATE,
    completed_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_onboarding_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id)
);

INSERT INTO onboarding
    (employee_id, status, started_date)
VALUES
    (1, 'IN_PROGRESS', '2026-09-21'),
    (2, 'PENDING', NULL);


-- =========================================================
-- 5. TASK TYPES
-- =========================================================

CREATE TABLE task_types (
    task_type_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    task_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO task_types
    (task_name, description)
VALUES
    ('HR Verification', 'Verify employee information and documents'),
    ('Manager Approval', 'Manager reviews and approves onboarding'),
    ('IT Setup', 'Setup laptop, email and required applications'),
    ('Training', 'Complete mandatory employee training');


-- =========================================================
-- 6. ONBOARDING TASKS
-- =========================================================

CREATE TABLE onboarding_tasks (
    task_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    onboarding_id BIGINT NOT NULL,
    task_type_id BIGINT NOT NULL,
    assigned_to BIGINT,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    due_date DATE,
    completed_date DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_task_onboarding
        FOREIGN KEY (onboarding_id)
        REFERENCES onboarding(onboarding_id),

    CONSTRAINT fk_task_type
        FOREIGN KEY (task_type_id)
        REFERENCES task_types(task_type_id),

    CONSTRAINT fk_task_user
        FOREIGN KEY (assigned_to)
        REFERENCES users(user_id)
);

INSERT INTO onboarding_tasks
    (onboarding_id, task_type_id, assigned_to, status, due_date)
VALUES
    (1, 1, 1, 'COMPLETED', '2026-09-22'),
    (1, 2, 2, 'IN_PROGRESS', '2026-09-23'),
    (1, 3, 1, 'PENDING', '2026-09-25'),
    (1, 4, 2, 'PENDING', '2026-09-28'),

    (2, 1, 1, 'PENDING', '2026-10-06'),
    (2, 2, 2, 'PENDING', '2026-10-07');


-- =========================================================
-- 7. ONBOARDING APPROVALS
-- =========================================================

CREATE TABLE onboarding_approvals (
    approval_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    onboarding_id BIGINT NOT NULL,
    approved_by BIGINT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    comments TEXT,
    approved_at TIMESTAMPTZ,

    CONSTRAINT fk_approval_onboarding
        FOREIGN KEY (onboarding_id)
        REFERENCES onboarding(onboarding_id),

    CONSTRAINT fk_approval_user
        FOREIGN KEY (approved_by)
        REFERENCES users(user_id)
);

INSERT INTO onboarding_approvals
    (onboarding_id, approved_by, status, comments, approved_at)
VALUES
    (1, 2, 'APPROVED',
     'Onboarding approved by manager',
     '2026-09-21 10:30:00+05:30'),

    (2, 2, 'PENDING',
     NULL,
     NULL);


-- =========================================================
-- VERIFY DATA
-- =========================================================

SELECT * FROM roles;

SELECT * FROM users;

SELECT * FROM employees;

SELECT * FROM onboarding;

SELECT * FROM task_types;

SELECT * FROM onboarding_tasks;

SELECT * FROM onboarding_approvals;