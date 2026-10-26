"""
MAVIS CHÚC BẠN NGỦ NGON - SQL DATABASE ENGINE (SQLite 3)
Provides ACID compliance, relational tables, foreign key constraints,
and high-performance indexing for users, diagnoses, and service logs.
Zero mock data: starts 100% clean for real user registrations.
"""

import os
import json
import sqlite3
from datetime import datetime
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Check for persistent volume paths commonly used on Render (/data or /var/data)
if os.path.exists('/data') and os.access('/data', os.W_OK):
    DATA_DIR = '/data'
elif os.path.exists('/var/data') and os.access('/var/data', os.W_OK):
    DATA_DIR = '/var/data'
else:
    DATA_DIR = BASE_DIR

DB_FILE = os.path.join(DATA_DIR, 'sleepsync.db')
SCHEMA_FILE = os.path.join(BASE_DIR, 'schema.sql')
SEED_FILE = os.path.join(BASE_DIR, 'seed.sql')


@contextmanager
def get_db():
    """Context manager for SQLite connections with foreign keys and dict-like rows."""
    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initializes tables and indexes from schema.sql, and seeds real user data if empty."""
    if os.path.exists(SCHEMA_FILE):
        with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
    else:
        # Fallback inline schema
        schema_sql = """
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
            health_conditions TEXT DEFAULT '["Sức khỏe ổn định"]',
            avatar_type TEXT DEFAULT 'programmer_laptop',
            verified INTEGER DEFAULT 1,
            streak_days INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            last_login_at TEXT,
            updated_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_users_phone ON users(phone);
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

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
        CREATE INDEX IF NOT EXISTS idx_service_usage_user ON service_usage(user_id);
        CREATE INDEX IF NOT EXISTS idx_service_usage_time ON service_usage(timestamp);

        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            user_name TEXT,
            score INTEGER NOT NULL DEFAULT 70,
            pillars TEXT NOT NULL,
            summary TEXT,
            answers TEXT,
            custom_answers TEXT,
            device TEXT DEFAULT 'Web Browser',
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_diagnoses_user ON diagnoses(user_id);
        CREATE INDEX IF NOT EXISTS idx_diagnoses_time ON diagnoses(timestamp);

        CREATE TABLE IF NOT EXISTS app_meta (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        """
    with get_db() as conn:
        conn.executescript(schema_sql)

        # Check if users table is empty (e.g. freshly deployed on Render)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]

        if user_count == 0 and os.path.exists(SEED_FILE):
            try:
                with open(SEED_FILE, 'r', encoding='utf-8') as f:
                    seed_sql = f.read()
                conn.executescript(seed_sql)
                print(f"[SQL Database] Seeded database with pre-configured users and clinical records from seed.sql.", flush=True)
            except Exception as e:
                print(f"[SQL Database] Warning during seed execution: {e}", flush=True)

    print(f"[SQL Database] Initialized successfully. File: {DB_FILE}", flush=True)


# ==============================================================================
# DATA SERIALIZERS & MAPPERS
# ==============================================================================

def row_to_user_dict(row):
    """Converts a SQLite row into a camelCase user dictionary for frontend compatibility."""
    if not row:
        return None
    
    # Parse JSON health conditions
    raw_conditions = row['health_conditions'] or '[]'
    try:
        health_conditions = json.loads(raw_conditions)
    except Exception:
        health_conditions = [raw_conditions] if raw_conditions else ['Sức khỏe ổn định']

    return {
        "id": row['id'],
        "username": row['username'] or row['phone'],
        "fullName": row['full_name'],
        "phone": row['phone'],
        "email": row['email'] or '',
        "password": row['password_hash'],
        "role": row['role'] or 'Thành viên Mavis',
        "bio": row['bio'] or 'Mục tiêu cải thiện chất lượng giấc ngủ sâu NREM 💤',
        "age": row['age'] or '28 tuổi',
        "gender": row['gender'] or 'Khác',
        "occupation": row['occupation'] or row['role'] or 'Tự do',
        "targetBedtime": row['target_bedtime'] or '23:00',
        "wakeTime": row['wake_time'] or '06:30',
        "fitnessLevel": row['fitness_level'] or 'Trung bình',
        "healthConditions": health_conditions,
        "avatarType": row['avatar_type'] or 'programmer_laptop',
        "verified": bool(row['verified']),
        "streakDays": row['streak_days'] or 1,
        "createdAt": row['created_at'],
        "lastLoginAt": row['last_login_at'] or row['created_at'],
        "updatedAt": row['updated_at']
    }


def row_to_log_dict(row):
    if not row:
        return None
    return {
        "id": row['id'],
        "userId": row['user_id'],
        "userName": row['user_name'],
        "serviceType": row['service_type'],
        "title": row['title'],
        "detail": row['detail'],
        "timestamp": row['timestamp'],
        "device": row['device'] or 'Web Browser',
        "icon": row['icon'] or 'fa-solid fa-circle-check',
        "badgeColor": row['badge_color'] or 'indigo'
    }


def row_to_diag_dict(row):
    if not row:
        return None
    
    def try_parse_json(val, default):
        if not val:
            return default
        try:
            return json.loads(val)
        except Exception:
            return default

    return {
        "id": row['id'],
        "userId": row['user_id'],
        "userName": row['user_name'],
        "score": row['score'],
        "pillars": try_parse_json(row['pillars'], {}),
        "summary": row['summary'] or '',
        "answers": try_parse_json(row['answers'], None),
        "customAnswers": try_parse_json(row['custom_answers'], {}),
        "device": row['device'] or 'Web Browser',
        "timestamp": row['timestamp']
    }


# ==============================================================================
# USER OPERATIONS
# ==============================================================================

def list_all_users():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC;")
        rows = cursor.fetchall()
        return [row_to_user_dict(r) for r in rows]


def get_user_by_id(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        row = cursor.fetchone()
        return row_to_user_dict(row)


def find_user_for_login(phone_or_id):
    """Flexible lookup matching phone, id, username, or email."""
    clean_val = phone_or_id.replace(" ", "").lower()
    with get_db() as conn:
        cursor = conn.cursor()
        # Direct match or case-insensitive match
        cursor.execute("""
            SELECT * FROM users 
            WHERE LOWER(id) = ? 
               OR LOWER(phone) = ? 
               OR REPLACE(LOWER(phone), ' ', '') = ?
               OR LOWER(username) = ? 
               OR LOWER(email) = ?
               OR LOWER(id) = ?
            LIMIT 1;
        """, (
            clean_val,
            phone_or_id.lower(),
            clean_val,
            clean_val,
            clean_val,
            "user_" + clean_val
        ))
        row = cursor.fetchone()
        if row:
            return row_to_user_dict(row)
        
        # Fallback full name match
        cursor.execute("SELECT * FROM users WHERE LOWER(full_name) = ? LIMIT 1;", (phone_or_id.lower(),))
        row = cursor.fetchone()
        return row_to_user_dict(row)


def create_user(user_data):
    """Creates a new real user in SQL database. Returns created user dict."""
    user_id = user_data.get("id") or ("user_" + str(int(datetime.now().timestamp())))
    full_name = user_data.get("fullName", "").strip()
    phone = user_data.get("phone", "").strip()
    username = user_data.get("username", phone).strip()
    email = user_data.get("email", "").strip()
    password = user_data.get("password", "123456").strip()
    role = user_data.get("role", "Thành viên Mavis")
    bio = user_data.get("bio", "Mục tiêu cải thiện chất lượng giấc ngủ sâu NREM 💤")
    age = user_data.get("age", "28 tuổi")
    gender = user_data.get("gender", "Khác")
    occupation = user_data.get("occupation", role)
    target_bedtime = user_data.get("targetBedtime", "23:00")
    wake_time = user_data.get("wakeTime", "06:30")
    fitness_level = user_data.get("fitnessLevel", "Trung bình")
    
    conds = user_data.get("healthConditions", ["Sức khỏe ổn định"])
    if isinstance(conds, list):
        conds_json = json.dumps(conds, ensure_ascii=False)
    else:
        conds_json = json.dumps([str(conds)], ensure_ascii=False)
        
    avatar_type = user_data.get("avatarType", "programmer_laptop")
    now_iso = datetime.now().isoformat()
    streak_days = int(user_data.get("streakDays", 1))

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (
                id, username, full_name, phone, email, password_hash,
                role, bio, age, gender, occupation, target_bedtime, wake_time,
                fitness_level, health_conditions, avatar_type, verified, streak_days,
                created_at, last_login_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id, username, full_name, phone, email, password,
            role, bio, age, gender, occupation, target_bedtime, wake_time,
            fitness_level, conds_json, avatar_type, 1, streak_days,
            now_iso, now_iso, now_iso
        ))
        
    return get_user_by_id(user_id)


def update_user(user_id, updates):
    """Updates user fields in SQL database."""
    current = get_user_by_id(user_id)
    if not current:
        return None

    full_name = updates.get("fullName", current["fullName"])
    phone = updates.get("phone", current["phone"])
    email = updates.get("email", current["email"])
    password = updates.get("password", current["password"])
    role = updates.get("role", current["role"])
    bio = updates.get("bio", current["bio"])
    age = updates.get("age", current["age"])
    gender = updates.get("gender", current["gender"])
    occupation = updates.get("occupation", current["occupation"])
    target_bedtime = updates.get("targetBedtime", current["targetBedtime"])
    wake_time = updates.get("wakeTime", current["wakeTime"])
    fitness_level = updates.get("fitnessLevel", current["fitnessLevel"])
    avatar_type = updates.get("avatarType", current["avatarType"])
    streak_days = updates.get("streakDays", current["streakDays"])
    last_login_at = updates.get("lastLoginAt", current["lastLoginAt"])

    conds = updates.get("healthConditions", current["healthConditions"])
    if isinstance(conds, list):
        conds_json = json.dumps(conds, ensure_ascii=False)
    else:
        conds_json = json.dumps([str(conds)], ensure_ascii=False)

    now_iso = datetime.now().isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET
                full_name = ?, phone = ?, email = ?, password_hash = ?,
                role = ?, bio = ?, age = ?, gender = ?, occupation = ?,
                target_bedtime = ?, wake_time = ?, fitness_level = ?,
                health_conditions = ?, avatar_type = ?, streak_days = ?,
                last_login_at = ?, updated_at = ?
            WHERE id = ?;
        """, (
            full_name, phone, email, password,
            role, bio, age, gender, occupation,
            target_bedtime, wake_time, fitness_level,
            conds_json, avatar_type, streak_days,
            last_login_at, now_iso, user_id
        ))

    return get_user_by_id(user_id)


def delete_user(user_id):
    """Deletes user by ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?;", (user_id,))
        return cursor.rowcount > 0


# ==============================================================================
# SERVICE LOGS OPERATIONS
# ==============================================================================

def add_service_log(log_data):
    """Inserts a service log entry into SQL database."""
    user_id = log_data.get("userId")
    user_name = log_data.get("userName") or "Người dùng"
    service_type = log_data.get("serviceType", "GENERAL_LOG")
    title = log_data.get("title", "Hoạt động hệ thống")
    detail = log_data.get("detail", "")
    timestamp = log_data.get("timestamp") or datetime.now().isoformat()
    device = log_data.get("device", "Web Browser")
    icon = log_data.get("icon", "fa-solid fa-circle-check")
    badge_color = log_data.get("badgeColor", "indigo")

    with get_db() as conn:
        cursor = conn.cursor()
        # Verify user_id exists in users table to satisfy foreign key constraint
        if user_id:
            cursor.execute("SELECT 1 FROM users WHERE id = ?;", (user_id,))
            if not cursor.fetchone():
                user_id = None

        cursor.execute("""
            INSERT INTO service_usage (
                user_id, user_name, service_type, title, detail,
                timestamp, device, icon, badge_color
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            user_id, user_name, service_type, title, detail,
            timestamp, device, icon, badge_color
        ))
        log_id = cursor.lastrowid
        cursor.execute("SELECT * FROM service_usage WHERE id = ?;", (log_id,))
        return row_to_log_dict(cursor.fetchone())


def list_service_logs(limit=150):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM service_usage ORDER BY timestamp DESC LIMIT ?;", (limit,))
        return [row_to_log_dict(r) for r in cursor.fetchall()]


# ==============================================================================
# DIAGNOSES OPERATIONS
# ==============================================================================

def save_diagnosis(diag_data):
    """Inserts a diagnosis record into SQL database."""
    diag_id = diag_data.get("id") or int(datetime.now().timestamp() * 1000)
    user_id = diag_data.get("userId")
    user_name = diag_data.get("userName") or "Người dùng"
    score = int(diag_data.get("score", 70))
    
    pillars = diag_data.get("pillars") or {}
    pillars_json = json.dumps(pillars, ensure_ascii=False) if isinstance(pillars, dict) else str(pillars)
    
    summary = diag_data.get("summary") or ""
    
    answers = diag_data.get("answers")
    answers_json = json.dumps(answers, ensure_ascii=False) if answers is not None else None
    
    custom_answers = diag_data.get("customAnswers")
    custom_json = json.dumps(custom_answers, ensure_ascii=False) if custom_answers is not None else None
    
    device = diag_data.get("device", "Web Browser")
    timestamp = diag_data.get("timestamp") or datetime.now().isoformat()

    with get_db() as conn:
        cursor = conn.cursor()
        # Verify user_id exists in users table to satisfy foreign key constraint
        if user_id:
            cursor.execute("SELECT 1 FROM users WHERE id = ?;", (user_id,))
            if not cursor.fetchone():
                user_id = None

        cursor.execute("""
            INSERT OR REPLACE INTO diagnoses (
                id, user_id, user_name, score, pillars, summary,
                answers, custom_answers, device, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            diag_id, user_id, user_name, score, pillars_json, summary,
            answers_json, custom_json, device, timestamp
        ))
        cursor.execute("SELECT * FROM diagnoses WHERE id = ?;", (diag_id,))
        return row_to_diag_dict(cursor.fetchone())


def list_diagnoses(user_id=None, limit=100):
    with get_db() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("SELECT * FROM diagnoses WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?;", (user_id, limit))
        else:
            cursor.execute("SELECT * FROM diagnoses ORDER BY timestamp DESC LIMIT ?;", (limit,))
        return [row_to_diag_dict(r) for r in cursor.fetchall()]


# ==============================================================================
# SYSTEM STATS & BACKUP
# ==============================================================================

def get_stats():
    """Calculates live platform stats using SQL aggregate queries."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users;")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM diagnoses;")
        total_diags = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM service_usage;")
        total_logs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM service_usage WHERE service_type LIKE '%GUARDRAIL%';")
        total_guardrails = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM service_usage WHERE service_type LIKE '%AI_CHAT%';")
        total_ai_chats = cursor.fetchone()[0]

        return {
            "totalUsers": total_users,
            "totalDiagnoses": total_diags,
            "totalAiChats": total_ai_chats,
            "totalGuardrailBlocks": total_guardrails,
            "totalLogs": total_logs,
            "lastSync": datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
            "serverStatus": "Online (Cơ sở dữ liệu SQL Hoạt động)",
            "databaseEngine": "SQLite 3 Relational SQL Database",
            "databaseFile": DB_FILE
        }


def export_full_database():
    """Exports full database as structured dict (matches existing backup format)."""
    users = list_all_users()
    logs = list_service_logs(limit=500)
    diags = list_diagnoses(limit=500)
    active_user = get_active_user_id()
    return {
        "users": users,
        "activeUserId": active_user,
        "serviceUsage": logs,
        "diagnoses": diags,
        "exportedAt": datetime.now().isoformat(),
        "databaseType": "SQLite3_SQL"
    }


def reset_database():
    """Clears all tables completely. Starts 100% clean with zero mock accounts."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM diagnoses;")
        cursor.execute("DELETE FROM service_usage;")
        cursor.execute("DELETE FROM users;")
        cursor.execute("DELETE FROM app_meta;")
    print("[SQL Database] Reset complete. Clean state with 0 sample accounts.", flush=True)
    return True


def get_active_user_id():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM app_meta WHERE key = 'active_user_id';")
        row = cursor.fetchone()
        return row[0] if row else None


def set_active_user_id(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        if user_id:
            cursor.execute("INSERT OR REPLACE INTO app_meta (key, value) VALUES ('active_user_id', ?);", (user_id,))
        else:
            cursor.execute("DELETE FROM app_meta WHERE key = 'active_user_id';")


# Initialize on import
init_db()
