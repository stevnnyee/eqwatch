import requests

USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/"


def fetch_earthquakes(min_magnitude=2.5, limit=100):
    params = {
        "format": "geojson",
        "minmagnitude": min_magnitude,
        "limit": limit,
        "orderby": "time",
    }
    response = requests.get(USGS_BASE_URL + "query", params=params)
    response.raise_for_status()
    return response.json()["features"]


def seed():
    print("Fetching earthquake data from USGS...")
    earthquakes = fetch_earthquakes()
    print(f"Fetched {len(earthquakes)} earthquakes")

    for eq in earthquakes:
        props = eq["properties"]
        coords = eq["geometry"]["coordinates"]
        # TODO: call insert_earthquake() once schema is defined
        print(f"  {props['mag']} - {props['place']}")
    print("Done.")


if __name__ == "__main__":
    seed()
