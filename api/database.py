from pathlib import Path
import sqlite3
import struct
from typing import Any

# Dynamic path pointing to data/Przystanki.sqlite
DATABASE_PATH: Path = (
    Path(__file__).resolve().parent.parent / "data" / "Przystanki.sqlite"
)
MINIMUM_WKB_POINT_BYTE_LENGTH: int = 21
DEFAULT_UNNAMED_STOP_LABEL: str = "Bez nazwy"


def parse_well_known_binary_point(
    binary_geometry: bytes,
) -> tuple[float, float]:
    """Unpack a Well-Known Binary (WKB) Point geometry into geographic coordinates.

    :param binary_geometry: Raw binary blob representing a WKB Point geometry.
    :type binary_geometry: bytes
    :return: A tuple containing longitude and latitude as ``(longitude, latitude)``.
    :rtype: tuple[float, float]
    :raises struct.error: If the binary geometry blob is malformed or shorter than 21 bytes.
    """
    longitude, latitude = struct.unpack("<dd", binary_geometry[5:21])
    return longitude, latitude


def determine_transit_stop_type(
    tram_flag: str | None,
    bus_flag: str | None,
) -> str:
    """Determine the public transit stop type based on OpenStreetMap (OSM) tags.

    :param tram_flag: Value of the OSM ``tram`` tag (e.g., ``"yes"`` or ``None``).
    :type tram_flag: str | None
    :param bus_flag: Value of the OSM ``bus`` tag (e.g., ``"yes"`` or ``None``).
    :type bus_flag: str | None
    :return: Localized stop category (``"tramwaj/autobus"``, ``"tramwaj"``,
             ``"autobus"``, or ``"inny"``).
    :rtype: str
    """
    is_tram_stop = tram_flag == "yes"
    is_bus_stop = bus_flag == "yes"

    if is_tram_stop and is_bus_stop:
        return "tramwaj/autobus"
    if is_tram_stop:
        return "tramwaj"
    if is_bus_stop:
        return "autobus"
    return "inny"


def fetch_all_transit_stops(
    database_path: Path = DATABASE_PATH,
) -> list[dict[str, Any]]:
    """Retrieve and parse all transit stops from the SQLite database.

    Connects to the specified SQLite database, queries the ``przystanki_sql``
    table, parses WKB point geometries, and normalizes stop metadata. Rows with
    missing or truncated geometry blobs are skipped.

    :param database_path: Filesystem path to the SQLite database file.
                          Defaults to ``DATABASE_PATH``.
    :type database_path: pathlib.Path
    :return: A list of dictionaries, each representing a normalized transit stop
             with keys: ``id``, ``name``, ``ref``, ``type``, ``shelter``,
             ``lat``, and ``lon``.
    :rtype: list[dict[str, Any]]
    :raises sqlite3.Error: If a database connection or query execution error occurs.
    """
    query = """
        SELECT
            ogc_fid,
            GEOMETRY,
            id,
            name,
            ref,
            shelter,
            tram,
            bus
        FROM przystanki_sql
    """

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        database_rows = cursor.fetchall()

    transit_stops: list[dict[str, Any]] = []

    for row in database_rows:
        binary_geometry: bytes | None = row["GEOMETRY"]
        if (
            not binary_geometry
            or len(binary_geometry) < MINIMUM_WKB_POINT_BYTE_LENGTH
        ):
            continue

        longitude, latitude = parse_well_known_binary_point(binary_geometry)
        stop_type = determine_transit_stop_type(row["tram"], row["bus"])

        transit_stops.append(
            {
                "id": row["id"] or str(row["ogc_fid"]),
                "name": row["name"] or DEFAULT_UNNAMED_STOP_LABEL,
                "ref": row["ref"],
                "type": stop_type,
                "shelter": row["shelter"] == "yes",
                "lat": latitude,
                "lon": longitude,
            }
        )

    return transit_stops