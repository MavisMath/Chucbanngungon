-- ==============================================================================
-- MAVIS CHÚC BẠN NGỦ NGON - SQL DATABASE SCHEMA
-- Compatible with SQLite, PostgreSQL, and MySQL
-- ==============================================================================

-- 1. Table: users (Hồ sơ người dùng thực tế)
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    full_name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    email TEXT,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'Thành viên Mavis',
    bio TEXT DEFAULT 'Mục tiêu cải thiện chất lượng giấc ngủ sâu NREM 💤',
    age TEXT DEFAULT '28 tuổi',
    gender TEXT DEFAULT 'Khác',
    occupation TEXT DEFAULT 'Tự do',
    target_bedtime TEXT DEFAULT '23:00',
    wake_time TEXT DEFAULT '06:30',
    fitness_level TEXT DEFAULT 'Trung bình',
    health_conditions TEXT DEFAULT '["Sức khỏe ổn định"]', -- JSON text array
    avatar_type TEXT DEFAULT 'programmer_laptop',
    verified INTEGER DEFAULT 1,
    streak_days INTEGER DEFAULT 1,
    created_at TEXT NOT NULL,
    last_login_at TEXT,
    updated_at TEXT
);

-- Index for fast user lookup during authentication
CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- 2. Table: service_usage (Nhật ký hoạt động & dịch vụ y khoa)
CREATE TABLE IF NOT EXISTS service_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    user_name TEXT,
    service_type TEXT NOT NULL,
    title TEXT NOT NULL,
    detail TEXT,
    timestamp TEXT NOT NULL,
    device TEXT DEFAULT 'Web Browser',
    icon TEXT DEFAULT 'fa-solid fa-circle-check',
    badge_color TEXT DEFAULT 'indigo',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Index for timeline queries
CREATE INDEX IF NOT EXISTS idx_service_usage_user ON service_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_service_usage_time ON service_usage(timestamp);

-- 3. Table: diagnoses (Kết quả khảo sát 5 trụ cột y khoa giấc ngủ)
CREATE TABLE IF NOT EXISTS diagnoses (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    user_name TEXT,
    score INTEGER NOT NULL DEFAULT 70,
    pillars TEXT NOT NULL,         -- JSON object: { p1_stress, p2_env, p3_lifestyle, p4_physio, p5_health }
    summary TEXT,
    answers TEXT,                 -- JSON object
    custom_answers TEXT,          -- JSON object (ý kiến tự gõ từ 'Khác...')
    device TEXT DEFAULT 'Web Browser',
    timestamp TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Index for user diagnoses
CREATE INDEX IF NOT EXISTS idx_diagnoses_user ON diagnoses(user_id);
CREATE INDEX IF NOT EXISTS idx_diagnoses_time ON diagnoses(timestamp);

-- 4. Table: app_meta (Cấu hình hệ thống & phiên hoạt động)
CREATE TABLE IF NOT EXISTS app_meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
