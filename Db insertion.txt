-- =========================================================================
-- SYSTEM IDENTITY: YUKTISHALA BOARD DATABASE SCHEMA INITIALISATION (FINAL)
-- ENGINE: SERVERLESS NEON POSTGRESQL (WITH ENCRYPTED PASSWORD STORAGE)
-- =========================================================================

-- 1. PURGE EXISTING STRUCTURE CONTEXTS (Clean slate execution)
DROP TABLE IF EXISTS bug_history_logs CASCADE;
DROP TABLE IF EXISTS bugs CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. CREATE USER MANAGEMENT ENTITY TABLE (WITH PASSWORD HASH)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255), -- Stores secure encrypted password strings
    role VARCHAR(50) NOT NULL CHECK (role IN ('Admin', 'Developer', 'QA'))
);

-- 3. CREATE CORE JIRA/KANBAN BUG TICKETS ENTITY TABLE
CREATE TABLE bugs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL CHECK (priority IN ('High', 'Medium', 'Low')),
    status VARCHAR(30) NOT NULL CHECK (status IN ('TO_DO', 'IN_PROGRESS', 'RESOLVED')),
    assigned_to INTEGER,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    
    -- Relational link connecting back to users table
    CONSTRAINT fk_bugs_assigned_user 
        FOREIGN KEY (assigned_to) 
        REFERENCES users(id) 
        ON DELETE SET NULL
);

-- 4. CREATE AUTONOMOUS AUDIT TRAIL LOG ENVIRONMENT TABLE
CREATE TABLE bug_history_logs (
    log_id SERIAL PRIMARY KEY,
    bug_id INTEGER NOT NULL,
    action_taken VARCHAR(50) NOT NULL CHECK (action_taken IN ('INSERT', 'UPDATE STATE', 'DELETE')),
    old_status VARCHAR(30),
    new_status VARCHAR(30),
    changed_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc'),
    
    -- Cascading link: If a bug is deleted, its history logs clean up automatically
    CONSTRAINT fk_logs_target_bug 
        FOREIGN KEY (bug_id) 
        REFERENCES bugs(id) 
        ON DELETE CASCADE
);

-- 5. INITIAL SEED INGESTION DATA HANDSHAKE (Sample data for instant testing)
INSERT INTO users (username, password_hash, role) VALUES 
('Sandeep Miriyala', '$2b$12$ExampleHashSecurePassword', 'Admin'),
('Ananya Rao', '$2b$12$ExampleHashDevPassword', 'Developer');

INSERT INTO bugs (title, description, priority, status, assigned_to) VALUES 
('Fix Neon DB Connection Pool Spillover', 'Serverless execution parameters exhausting connections under load.', 'High', 'TO_DO', 1);


INSERT INTO bug_history_logs (bug_id, action_taken, old_status, new_status) VALUES 
-- రికార్డ్ 1: ఒక బగ్‌ను కొత్తగా క్రియేట్ చేసినప్పుడు పడే లాగ్
(1, 'INSERT', NULL, 'TO_DO'),

-- రికార్డ్ 2: డెవలపర్ పని ప్రారంభించినప్పుడు స్టేటస్ మారిన లాగ్
(1, 'UPDATE STATE', 'TO_DO', 'IN_PROGRESS'),

-- రికార్డ్ 3: బగ్ పూర్తిగా ఫిక్స్ అయి క్లోజ్ అయినప్పుడు పడే లాగ్
(1, 'UPDATE STATE', 'IN_PROGRESS', 'RESOLVED');


select * from  users
select * from  bugs
select * from bug_history_logs