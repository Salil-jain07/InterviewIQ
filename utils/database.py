import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "database", "interviewiq.db")


# =========================
# CREATE TABLES
# =========================
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS interviews(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    subject TEXT,
    question TEXT,
    answer TEXT,
    score REAL,
    grade TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("PRAGMA table_info(interviews)")
print(cursor.fetchall())

conn.commit()
conn.close()

print("Database created successfully!")


# =========================
# REGISTER USER
# =========================
def register_user(name, email, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


# =========================
# LOGIN USER
# =========================
def login_user(email, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user


# =========================
# SAVE INTERVIEW
# =========================
def save_interview(user_email,subject, question, answer, score, grade):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ---- SAFETY FIX ----
    try:
        score = float(score)
    except:
        score = 0.0

    score = max(0, min(100, score))  # HARD LOCK 0–100

    if grade is None:
        grade = "N/A"

    cursor.execute("""
        INSERT INTO interviews
        (user_email, subject, question, answer, score, grade)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_email,
        subject,
        question,
        answer,
        score,
        grade
    ))

    conn.commit()
    conn.close()

