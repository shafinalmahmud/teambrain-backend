import sqlite3
import json

conn = sqlite3.connect("idempotency.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS idempotency (
    key TEXT PRIMARY KEY,
    status TEXT,
    result TEXT
);
""")
conn.commit()

def is_done(key: str):
    row = cur.execute("SELECT result FROM idempotency WHERE key=?", (key,)).fetchone()
    return json.loads(row[0]) if row else None

def mark_done(key: str, result: dict):
    cur.execute(
        "INSERT OR REPLACE INTO idempotency (key, status, result) VALUES (?, ?, ?)",
        (key, "done", json.dumps(result))
    )
    conn.commit()