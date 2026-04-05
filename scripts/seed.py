"""
Fetch recent earthquakes from USGS FDSNWS and insert into the database.

Requires backend/.env with DB_* (see backend/.env.example) and a running MySQL
instance with schema applied (e.g. `make db` after `make db-reset` if you change schema.sql).
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "backend"))

USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
DEFAULT_PARAMS = {
    "format": "geojson",
    "limit": 1000,
    "minmagnitude": 2.5,
}


def fetch_earthquakes() -> list[dict]:
    response = requests.get(USGS_BASE_URL, params=DEFAULT_PARAMS, timeout=60)
    response.raise_for_status()
    data = response.json()

    rows: list[dict] = []
    for feature in data.get("features", []):
        row = _feature_to_row(feature)
        if row is not None:
            rows.append(row)
    return rows


def _feature_to_row(feature: dict) -> dict | None:
    props = feature.get("properties") or {}
    geometry = feature.get("geometry") or {}
    coords = geometry.get("coordinates") or []
    if len(coords) < 3:
        return None

    lon, lat, depth = float(coords[0]), float(coords[1]), float(coords[2])
    mag = props.get("mag")
    if mag is None:
        return None

    t_ms = props.get("time")
    if t_ms is None:
        return None

    place = props.get("place") or "Unknown"
    occurred = datetime.fromtimestamp(t_ms / 1000.0, tz=timezone.utc).replace(
        tzinfo=None
    )

    return {
        "magnitude": float(mag),
        "depth": depth,
        "latitude": lat,
        "longitude": lon,
        "location_name": place[:255],
        "occurred_at": occurred,
    }


def seed() -> None:
    from services import earthquakes as eq_service

    rows = fetch_earthquakes()
    for row in rows:
        eq_service.insert_earthquake(row)
    print(f"Inserted {len(rows)} earthquakes.")


if __name__ == "__main__":
    seed()
