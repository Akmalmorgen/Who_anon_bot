# who_anon_bot/db/users.py

from .database import cursor, conn


def ensure_user(user_id: int, first_name: str):
    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id, first_name) VALUES(?,?)",
        (user_id, first_name)
    )
    conn.commit()


def get_state(user_id: int):
    cursor.execute("SELECT state FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else "main_menu"


def set_state(user_id: int, state: str):
    cursor.execute("UPDATE users SET state = ? WHERE user_id = ?", (state, user_id))
    conn.commit()


def set_gender(user_id: int, gender: str):
    cursor.execute("UPDATE users SET gender = ? WHERE user_id = ?", (gender, user_id))
    conn.commit()


def is_banned(user_id: int) -> bool:
    cursor.execute("SELECT banned FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row and row[0] == 1


def ban_user(target_id: int):
    cursor.execute("UPDATE users SET banned = 1 WHERE user_id = ?", (target_id,))
    conn.commit()


def unban_user(target_id: int):
    cursor.execute("UPDATE users SET banned = 0 WHERE user_id = ?", (target_id,))
    conn.commit()


def get_all_users():
    cursor.execute("SELECT user_id FROM users")
    return [u[0] for u in cursor.fetchall()]
