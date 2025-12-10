# who_anon_bot/db/roulette.py

from .database import cursor, conn

roulette_queue = {"M": [], "F": []}


def add_to_queue(user_id: int, gender: str):
    roulette_queue[gender].append(user_id)


def remove_from_queue(user_id: int):
    for g in ["M", "F"]:
        if user_id in roulette_queue[g]:
            roulette_queue[g].remove(user_id)


def get_pair(gender: str):
    opposite = "F" if gender == "M" else "M"
    if roulette_queue[opposite]:
        return roulette_queue[opposite].pop(0)
    return None


def set_pair(u1: int, u2: int):
    cursor.execute("INSERT OR REPLACE INTO active_chats(user_id, partner_id) VALUES(?,?)", (u1, u2))
    cursor.execute("INSERT OR REPLACE INTO active_chats(user_id, partner_id) VALUES(?,?)", (u2, u1))
    conn.commit()


def get_partner(user_id: int):
    cursor.execute("SELECT partner_id FROM active_chats WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else None


def remove_pair(user_id: int):
    partner = get_partner(user_id)
    if partner:
        cursor.execute("DELETE FROM active_chats WHERE user_id IN (?,?)", (user_id, partner))
        conn.commit()
        return partner
    return None
