import sys
import os
import requests
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from database import get_db

USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/"


def fetch_earthquakes():
    '''Fetches the 100 most recent earthquakes from the USGS API'''
    response = requests.get(USGS_BASE_URL + "query", params={
        "format": "geojson",
        "limit": 100,
        "orderby": "time",
    })
    response.raise_for_status()
    return response.json()["features"]


def seed():
    '''Inserts fetched earthquakes into the Earthquakes table'''
    earthquakes = fetch_earthquakes()

    insert_query = """
        INSERT INTO Earthquakes (magnitude, depth, latitude, longitude, location_name, occurred_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    with get_db() as conn:
        cursor = conn.cursor()
        for eq in earthquakes:
            props = eq["properties"]
            coords = eq["geometry"]["coordinates"]
            cursor.execute(insert_query, (
                props["mag"],
                max(coords[2], 0),
                coords[1],
                coords[0],
                props.get("place"),
                datetime.fromtimestamp(props["time"] / 1000, tz=timezone.utc),
            ))
        conn.commit()
        print(f"Inserted {cursor.rowcount} earthquakes.")


if __name__ == "__main__":
    seed()
