from database import get_db, query
from fastapi import HTTPException
from mysql.connector import DatabaseError


def get_all_regions():
    """Returns a list of all regions (region_id, name, min_lat, max_lat, min_lon, max_lon)"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_all_regions"))
        return cursor.fetchall()


def get_region(region_id: int):
    """Returns a single region by region_id, or None if not found"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_region"), (region_id,))
        return cursor.fetchone()


def create_region(body):
    """Returns the new region's region_id"""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                query("create_region"),
                (body.name, body.min_lat, body.max_lat, body.min_lon, body.max_lon),
            )
            conn.commit()
            return {"region_id": cursor.lastrowid}
        except DatabaseError as e:
            if e.errno == 3819:
                raise HTTPException(
                    status_code=422,
                    detail="Check constraint violated: ensure min_lat < max_lat and min_lon < max_lon",
                )
            raise


def delete_region(region_id: int):
    """Returns whether a row was deleted"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query("delete_region"), (region_id,))
        conn.commit()
        return {"deleted": cursor.rowcount > 0}
