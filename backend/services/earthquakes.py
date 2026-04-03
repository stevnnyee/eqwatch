from database import get_db


def get_all_earthquakes():
    pass


def get_earthquake(earthquake_id: int):
    pass


def insert_earthquake(eq: dict) -> int:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO earthquakes (
                magnitude, depth, latitude, longitude, location_name, `timestamp`
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                eq["magnitude"],
                eq["depth"],
                eq["latitude"],
                eq["longitude"],
                eq["location_name"],
                eq["timestamp"],
            ),
        )
        conn.commit()
        return cursor.lastrowid
