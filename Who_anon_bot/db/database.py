# who_anon_bot/db/database.py

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "who_anon.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


def init_db():
    """Создание всех таблиц при запуске."""

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        first_name TEXT,
        gender TEXT,
        link_id TEXT,
        banned INTEGER DEFAULT 0,
        state TEXT DEFAULT 'main_menu'
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS links(
        link_id TEXT PRIMARY KEY,
        owner_id INTEGER,
        created_at TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS anon_sessions(
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        anon_user_id INTEGER,
        owner_id INTEGER,
        anon_tag TEXT,
        created_at TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS message_map(
        owner_message_id INTEGER PRIMARY KEY,
        session_id INTEGER,
        owner_id INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS active_chats(
        user_id INTEGER PRIMARY KEY,
        partner_id INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reporter_id INTEGER,
        reported_id INTEGER,
        offender_anon_tag TEXT,
        reason TEXT,
        date TEXT,
        chat_type TEXT
    );
    """)

    conn.commit()
