from typing import Any
from fastapi.testclient import TestClient
from api.main import app

WROCLAW_MARKET_SQUARE_LATITUDE: float = 51.1098
WROCLAW_MARKET_SQUARE_LONGITUDE: float = 17.0315
HTTP_OK_STATUS_CODE: int = 200

test_client = TestClient(app)


def test_health_check_returns_ok_status() -> None:
    """Verify that the root health check endpoint returns an OK status.

    :return: None
    :rtype: None
    :raises AssertionError: If the HTTP status code is not 200 or the response
                            status field is not ``"ok"``.
    """
    response = test_client.get("/")
    assert response.status_code == HTTP_OK_STATUS_CODE

    response_payload: dict[str, Any] = response.json()
    assert response_payload["status"] == "ok"


def test_retrieve_all_stops_returns_valid_geojson_collection() -> None:
    """Verify that ``/stops`` returns a non-empty GeoJSON FeatureCollection.

    :return: None
    :rtype: None
    :raises AssertionError: If the HTTP status code is not 200, the GeoJSON type
                            is invalid, or the features list is missing/empty.
    """
    response = test_client.get("/stops")
    assert response.status_code == HTTP_OK_STATUS_CODE

    geojson_payload: dict[str, Any] = response.json()
    assert geojson_payload["type"] == "FeatureCollection"
    assert "features" in geojson_payload
    assert len(geojson_payload["features"]) > 0


def test_retrieve_transit_stop_statistics_returns_positive_counts() -> None:
    """Verify that ``/stats`` returns aggregated statistics with positive totals.

    :return: None
    :rtype: None
    :raises AssertionError: If the HTTP status code is not 200, total stops is
                            not greater than zero, or ``by_type`` is missing.
    """
    response = test_client.get("/stats")
    assert response.status_code == HTTP_OK_STATUS_CODE

    statistics_payload: dict[str, Any] = response.json()
    assert statistics_payload["total_stops"] > 0
    assert "by_type" in statistics_payload


def test_find_nearest_transit_stop_in_wroclaw_city_center() -> None:
    """Verify that ``/stops/nearest`` returns a valid stop near Wrocław Market Square.

    :return: None
    :rtype: None
    :raises AssertionError: If the HTTP status code is not 200, required keys are
                            missing, or the calculated distance is negative.
    """
    response = test_client.get(
        "/stops/nearest",
        params={
            "lat": WROCLAW_MARKET_SQUARE_LATITUDE,
            "lon": WROCLAW_MARKET_SQUARE_LONGITUDE,
        },
    )
    assert response.status_code == HTTP_OK_STATUS_CODE

    nearest_stop_payload: dict[str, Any] = response.json()
    assert "nearest_stop" in nearest_stop_payload
    assert "distance_meters" in nearest_stop_payload
    assert nearest_stop_payload["distance_meters"] >= 0.0