import sqlite3
from contextlib import contextmanager
from datetime import datetime

import config


@contextmanager
def db():
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                kind TEXT NOT NULL,
                budget INTEGER NOT NULL,
                details TEXT NOT NULL,
                preferences TEXT,
                result TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def create_user(username, email, password_hash):
    with db() as conn:
        conn.execute(
            "INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, password_hash, now()),
        )


def get_user_by_username(username):
    with db() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    return dict(row) if row else None


def get_user_by_id(user_id):
    with db() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def add_history(user_id, kind, budget, details, preferences, result):
    with db() as conn:
        conn.execute(
            """INSERT INTO history (user_id, kind, budget, details, preferences, result, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, kind, budget, details, preferences, result, now()),
        )


def get_history(user_id, limit=None):
    sql = "SELECT * FROM history WHERE user_id = ? ORDER BY id DESC"
    params = [user_id]
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    with db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def get_history_item(user_id, item_id):
    with db() as conn:
        row = conn.execute(
            "SELECT * FROM history WHERE id = ? AND user_id = ?", (item_id, user_id)
        ).fetchone()
    return dict(row) if row else None
