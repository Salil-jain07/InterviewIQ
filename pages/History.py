import streamlit as st
import sqlite3
import pandas as pd
import os

# -------------------------
# LOGIN CHECK
# -------------------------
if "logged_in" not in st.session_state:
    st.error("Please login first.")
    st.stop()


# =========================
# DB PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, "database", "interviewiq.db")

# =========================
# LOAD DATA SAFELY
# =========================

conn = sqlite3.connect(db_path)

email = st.session_state.user_email

df = pd.read_sql_query(
    """
    SELECT
        subject,
        question,
        answer,
        score,
        grade,
        timestamp
    FROM interviews
    WHERE user_email = ?
    ORDER BY timestamp DESC
    """,
    conn,
    params=(email,)
)

conn.close()

# =========================
# CLEAN TEXT (IMPORTANT FIX)
# =========================
def clean_text(x):
    if x is None:
        return ""
    try:
        return str(x).encode("utf-8", "ignore").decode("utf-8")
    except:
        return ""

for col in df.columns:
    df[col] = df[col].apply(clean_text)

# =========================
# FIX SCORE TYPE (optional but safe)
# =========================
if "score" in df.columns:
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0)
    df["score"] = df["score"].clip(0, 100)

# =========================
# UI
# =========================
st.title("📊 Mock Interview History")
df = df.reset_index(drop=True)
df.index = range(len(df), 0, -1)
st.dataframe(df)