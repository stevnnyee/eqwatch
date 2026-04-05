from database import get_db, query
from fastapi import HTTPException
from mysql.connector import IntegrityError


def get_all_users():
    '''Returns a list of all users (user_id, first_name, last_name, email, created_at)'''
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_all_users"))
        return cursor.fetchall()


def get_user(user_id: int):
    '''Returns a single user by user_id, or None if not found'''
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_user"), (user_id,))
        return cursor.fetchone()


def create_user(body):
    '''Returns the new user's user_id'''
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query("create_user"), (body.first_name, body.last_name, body.email, body.password))
            conn.commit()
            return {"user_id": cursor.lastrowid}
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Email already in use")


def delete_user(user_id: int):
    '''Returns whether a row was deleted'''
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query("delete_user"), (user_id,))
        conn.commit()
        return {"deleted": cursor.rowcount > 0}
