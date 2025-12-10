# who_anon_bot/db/links.py

import random
from datetime import datetime
from .database import cursor, conn


def get_or_create_link(user_id: int) -> str:
    cursor.execute("SELECT link_id FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row and row[0]:
        return row[0]

    # создать новую
    link_id = str(random.randint(100000, 999999))

    cursor.execute("UPDATE users SET link_id = ? WHERE user_id = ?", (link_id, user_id))
    cursor.execute(
        "INSERT OR REPLACE INTO links(link_id, owner_id, created_at) VALUES(?,?,?)",
        (link_id, user_id, datetime.utcnow().isoformat())
    )
    conn.commit()

    return link_id


def change_link(user_id: int) -> str:
    cursor.execute("SELECT link_id FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    old = row[0] if row else None

    if old:
        cursor.execute("DELETE FROM links WHERE link_id = ?", (old,))
        cursor.execute("UPDATE users SET link_id = NULL WHERE link_id = ?", (old,))
        conn.commit()

    new_link = str(random.randint(100000, 999999))

    cursor.execute("UPDATE users SET link_id = ? WHERE user_id = ?", (new_link, user_id))
    cursor.execute(
        "INSERT OR REPLACE INTO links(link_id, owner_id, created_at) VALUES(?,?,?)",
        (new_link, user_id, datetime.utcnow().isoformat())
    )
    conn.commit()

    return new_link


def get_link_owner(link_id: str):
    cursor.execute("SELECT owner_id FROM links WHERE link_id = ?", (link_id,))
    row = cursor.fetchone()
    return row[0] if row else None
