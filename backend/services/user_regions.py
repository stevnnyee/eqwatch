from database import get_db, query
from fastapi import HTTPException
from mysql.connector import DatabaseError


def get_regions_for_user(user_id: int):
    '''Returns a list of all regions associated with the given user'''
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_regions_for_user"), (user_id,))
        return cursor.fetchall()


def add_user_region(body):
    '''Returns the user_id and region_id of the newly created association'''
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(query("add_user_region"), (body.user_id, body.region_id))
            conn.commit()
            return {"user_id": body.user_id, "region_id": body.region_id}
        except DatabaseError as e:
            if e.errno == 1062:
                raise HTTPException(status_code=422, detail="user_id, region_id pair already exists.")
            elif e.errno == 1452:
                raise HTTPException(status_code=422, detail="user_id and/or region_id aren't valid.")
            raise

def remove_user_region(user_id: int, region_id: int):
    '''Returns whether a row was deleted'''
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query("remove_user_region"), (user_id, region_id))
        conn.commit()
        return {"deleted": cursor.rowcount > 0}
