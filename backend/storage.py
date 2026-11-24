# backend/storage.py
from pathlib import Path

import psycopg
from dotenv import dotenv_values
from psycopg.rows import dict_row

DATABASE_URL = dotenv_values(Path(__file__).with_name(".env")).get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("请在 backend/.env 里配置 DATABASE_URL")

def get_conn(row_factory=dict_row):
    return psycopg.connect(DATABASE_URL, row_factory=row_factory)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id SERIAL PRIMARY KEY,
        session_id TEXT,
        text TEXT,
        score REAL,
        label TEXT,
        pinyin TEXT,
        created_at TEXT
    )
    """)

    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_history_session_created "
        "ON history(session_id, created_at)"
    )
    conn.commit()
    conn.close()


def save_record(session_id, record):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (session_id, text, score, label, pinyin, created_at)"
        " VALUES (%s, %s, %s, %s, %s, %s)",
        [session_id, record["text"], record["score"],
         record["label"], record["pinyin"], record["created_at"]],
    )

    conn.commit()
    conn.close()

def get_history(session_id, limit):
    conn = get_conn()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT * FROM history WHERE session_id = %s ORDER BY created_at DESC LIMIT %s",
        [session_id, limit],
    ).fetchall()
    conn.close()

    records = []
    for row in rows:
        records.append(dict(row))
    return records
