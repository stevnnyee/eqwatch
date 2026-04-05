from database import get_db, query


def get_all_earthquakes():
    """Returns a list of all earthquakes (eq_id, magnitude, depth, latitude, longitude, location_name, occurred_at)"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_all_earthquakes"))
        return cursor.fetchall()


def get_earthquake(earthquake_id: int):
    """Returns a single earthquake by eq_id, or None if not found"""
    with get_db() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query("get_earthquake"), (earthquake_id,))
        return cursor.fetchone()


def insert_earthquake(eq: dict):
    """Returns the new earthquake's eq_id"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            query("insert_earthquake"),
            (
                eq["magnitude"],
                eq["depth"],
                eq["latitude"],
                eq["longitude"],
                eq.get("location_name"),
                eq["occurred_at"],
            ),
        )
        conn.commit()
        return {"eq_id": cursor.lastrowid}
