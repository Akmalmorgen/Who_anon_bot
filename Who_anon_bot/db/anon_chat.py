# who_anon_bot/db/anon_chat.py

from datetime import datetime
import random
from .database import cursor, conn


def create_session(anon_user_id: int, owner_id: int) -> int:
    anon_tag = str(random.randint(1000, 9999))

    cursor.execute(
        """
        INSERT INTO anon_sessions(anon_user_id, owner_id, anon_tag, created_at)
        VALUES(?,?,?,?)
        """,
        (anon_user_id, owner_id, anon_tag, datetime.utcnow().isoformat())
    )

    conn.commit()
    return cursor.lastrowid


def get_session(session_id: int):
    cursor.execute(
        "SELECT session_id, anon_user_id, owner_id, anon_tag FROM anon_sessions WHERE session_id = ?",
        (session_id,)
    )
    return cursor.fetchone()


def map_message(owner_message_id: int, session_id: int, owner_id: int):
    cursor.execute(
        "INSERT OR REPLACE INTO message_map(owner_message_id, session_id, owner_id) VALUES(?,?,?)",
        (owner_message_id, session_id, owner_id)
    )
    conn.commit()


def get_session_by_owner_message(message_id: int):
    cursor.execute(
        "SELECT session_id, owner_id FROM message_map WHERE owner_message_id = ?",
        (message_id,)
    )
    return cursor.fetchone()
