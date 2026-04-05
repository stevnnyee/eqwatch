from database import get_db, query
from fastapi import HTTPException
from mysql.connector import DatabaseError


def get_preferences_for_user(user_id: int):
    """Returns a list of all notification preferences for the given user"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_preferences_for_user"), (user_id,))
        return cursor.fetchall()


def create_preference(body):
    """Returns the new preference's pref_id"""
    with get_db() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                query("create_preference"),
                (body.user_id, body.min_magnitude, body.notify_email),
            )
            conn.commit()
            return {"pref_id": cursor.lastrowid}
        except DatabaseError as e:
            if e.errno == 3819:
                raise HTTPException(
                    status_code=422, detail="Magnitude is between -2 and 10."
                )
            raise


def delete_preference(pref_id: int):
    """Returns whether a row was deleted"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query("delete_preference"), (pref_id,))
        conn.commit()
        return {"deleted": cursor.rowcount > 0}
