# who_anon_bot/db/complaints.py

from datetime import datetime
from .database import cursor, conn


def add_complaint(reporter_id, reported_id, anon_tag, reason, chat_type):
    cursor.execute(
        """
        INSERT INTO complaints(reporter_id, reported_id, offender_anon_tag, reason, date, chat_type)
        VALUES(?,?,?,?,?,?)
        """,
        (reporter_id, reported_id, anon_tag, reason, datetime.utcnow().isoformat(), chat_type)
    )
    conn.commit()


def get_complaints():
    cursor.execute("SELECT id, reporter_id, reported_id, offender_anon_tag, reason, date FROM complaints ORDER BY id DESC")
    return cursor.fetchall()


def clear_complaints():
    cursor.execute("DELETE FROM complaints")
    conn.commit()
