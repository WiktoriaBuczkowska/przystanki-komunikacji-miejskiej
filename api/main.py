import math
from typing import Any
from fastapi import FastAPI, HTTPException, Query
from api.database import fetch_all_transit_stops

EARTH_RADIUS_METERS: float = 6_371_000.0

app = FastAPI(
    title="Wrocław Transit API",
    description="API do obsługi i analizy przystanków komunikacji miejskiej we Wrocławiu",
    version="1.0.0",
)


def calculate_haversine_distance(
    first_latitude: float,
    first_longitude: float,
    second_latitude: float,
    second_longitude: float,
) -> float:
    """Calculate the great-circle distance in meters between two geographic points.

    Uses the Haversine formula assuming a spherical Earth with radius
    ``EARTH_RADIUS_METERS``.

    :param first_latitude: Latitude of the first point in decimal degrees.
    :type first_latitude: float
    :param first_longitude: Longitude of the first point in decimal degrees.
    :type first_longitude: float
    :param second_latitude: Latitude of the second point in decimal degrees.
    :type second_latitude: float
    :param second_longitude: Longitude of the second point in decimal degrees.
    :type second_longitude: float
    :return: Distance between the two coordinates in meters.
    :rtype: float
    """
    first_latitude_radians = math.radians(first_latitude)
    second_latitude_radians = math.radians(second_latitude)
    latitude_delta_radians = math.radians(second_latitude - first_latitude)
    longitude_delta_radians = math.radians(second_longitude - first_longitude)

    haversine_component = (
        math.sin(latitude_delta_radians / 2.0) ** 2
        + math.cos(first_latitude_radians)
        * math.cos(second_latitude_radians)
        * math.sin(longitude_delta_radians / 2.0) ** 2
    )
    central_angle = 2.0 * math.atan2(
        math.sqrt(haversine_component), math.sqrt(1.0 - haversine_component)
    )

    return EARTH_RADIUS_METERS * central_angle


@app.get("/", tags=["Health"])
def check_service_health() -> dict[str, str]:
    """Perform a basic health check of the API service.

    :return: Service status and documentation URL path.
    :rtype: dict[str, str]
    """
    return {"status": "ok", "docs": "/docs"}


@app.get("/stops", tags=["Stops"])
def retrieve_all_stops_geojson() -> dict[str, Any]:
    """Retrieve all transit stops formatted as a GeoJSON FeatureCollection.

    :return: A GeoJSON ``FeatureCollection`` dictionary containing point features
             for every valid transit stop.
    :rtype: dict[str, Any]
    """
    transit_stops = fetch_all_transit_stops()
    geojson_features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [stop["lon"], stop["lat"]],
            },
            "properties": {
                "id": stop["id"],
                "name": stop["name"],
                "ref": stop["ref"],
                "type": stop["type"],
                "shelter": stop["shelter"],
            },
        }
        for stop in transit_stops
    ]
    return {"type": "FeatureCollection", "features": geojson_features}


@app.get("/stats", tags=["Statistics"])
def retrieve_transit_stop_statistics() -> dict[str, Any]:
    """Compute summary statistics for all transit stops in the dataset.

    Aggregates the total number of stops, breakdown by transit category,
    and counts of stops with and without shelters.

    :return: Dictionary containing aggregated stop statistics.
    :rtype: dict[str, Any]
    """
    transit_stops = fetch_all_transit_stops()
    stops_by_type: dict[str, int] = {}
    stops_with_shelter_count = 0

    for stop in transit_stops:
        stop_type: str = stop["type"]
        stops_by_type[stop_type] = stops_by_type.get(stop_type, 0) + 1
        if stop["shelter"]:
            stops_with_shelter_count += 1

    total_stops_count = len(transit_stops)

    return {
        "total_stops": total_stops_count,
        "by_type": stops_by_type,
        "with_shelter": stops_with_shelter_count,
        "without_shelter": total_stops_count - stops_with_shelter_count,
    }


@app.get("/stops/nearest", tags=["Stops"])
def find_nearest_transit_stop(
    latitude: float = Query(
        ...,
        alias="lat",
        ge=-90.0,
        le=90.0,
        description="Szerokość geograficzna (np. 51.10788)",
    ),
    longitude: float = Query(
        ...,
        alias="lon",
        ge=-180.0,
        le=180.0,
        description="Długość geograficzna (np. 17.03853)",
    ),
) -> dict[str, Any]:
    """Find the closest transit stop to the provided geographic coordinates.

    :param latitude: Target latitude in decimal degrees (query parameter ``lat``).
    :type latitude: float
    :param longitude: Target longitude in decimal degrees (query parameter ``lon``).
    :type longitude: float
    :return: Dictionary containing the nearest stop metadata and rounded distance
             in meters.
    :rtype: dict[str, Any]
    :raises HTTPException: With status code 404 if no transit stops exist in the database.
    """
    transit_stops = fetch_all_transit_stops()
    if not transit_stops:
        raise HTTPException(
            status_code=404,
            detail="Brak przystanków w bazie danych",
        )

    nearest_stop = min(
        transit_stops,
        key=lambda stop: calculate_haversine_distance(
            latitude, longitude, stop["lat"], stop["lon"]
        ),
    )
    distance_in_meters = calculate_haversine_distance(
        latitude, longitude, nearest_stop["lat"], nearest_stop["lon"]
    )

    return {
        "nearest_stop": nearest_stop,
        "distance_meters": round(distance_in_meters, 1),
    }