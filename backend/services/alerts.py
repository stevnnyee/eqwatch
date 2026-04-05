from database import get_db, query
from fastapi import HTTPException
from mysql.connector import DatabaseError


def get_all_alerts():
    """Returns a list of all alerts (alert_id, user_id, eq_id, sent_at)"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_all_alerts"))
        return cursor.fetchall()


def create_alert(body):
    """Returns the new alert's alert_id"""
    with get_db() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query("create_alert"), (body.user_id, body.eq_id))
            conn.commit()
            return {"alert_id": cursor.lastrowid}
        except DatabaseError as e:
            if e.errno == 1062:
                raise HTTPException(
                    status_code=422, detail="user_id, eq_id pair already exists."
                )
            elif e.errno == 1452:
                raise HTTPException(
                    status_code=422, detail="user_id and/or eq_id aren't valid."
                )
            raise


def delete_alert(alert_id: int):
    """Returns whether a row was deleted"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query("delete_alert"), (alert_id,))
        conn.commit()
        return {"deleted": cursor.rowcount > 0}
