"""Tiny SQLite helper. Only text results are stored - NEVER the uploaded image."""
import os
import sqlite3
from contextlib import contextmanager

DB_PATH = os.getenv("DB_PATH", "history.db")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read rows like dictionaries
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                label TEXT,
                category TEXT,
                confidence REAL,
                uncertain INTEGER,
                feedback INTEGER   -- NULL = none, 1 = correct, 0 = wrong
            )"""
        )


def add_entry(label, category, confidence, uncertain):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO history (label, category, confidence, uncertain) VALUES (?,?,?,?)",
            (label, category, confidence, int(uncertain)),
        )
        return cur.lastrowid


def list_entries(limit=50):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


def clear_entries():
    with get_conn() as conn:
        conn.execute("DELETE FROM history")


def set_feedback(entry_id, correct):
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE history SET feedback=? WHERE id=?", (int(correct), entry_id)
        )
        return cur.rowcount > 0
