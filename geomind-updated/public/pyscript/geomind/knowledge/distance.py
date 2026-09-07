"""
Geodesic distance calculation, bearing, and travel route estimations.
"""
import math
from typing import Optional, Tuple
from geomind.core.types import GeoCoord, DistanceResult


EARTH_RADIUS_KM = 6371.0088
KM_TO_MILES = 0.62137119


def haversine_distance_km(coord1: GeoCoord, coord2: GeoCoord) -> float:
    """Calculates the great-circle distance between two points on the Earth's surface in km."""
    lat1_rad = math.radians(coord1.lat)
    lon1_rad = math.radians(coord1.lon)
    lat2_rad = math.radians(coord2.lat)
    lon2_rad = math.radians(coord2.lon)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = (math.sin(dlat / 2.0) ** 2 +
         math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(dlon / 2.0) ** 2))
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return EARTH_RADIUS_KM * c


def calculate_bearing(coord1: GeoCoord, coord2: GeoCoord) -> float:
    """Calculates the initial compass bearing (azimuth) from coord1 to coord2 in degrees [0, 360)."""
    lat1_rad = math.radians(coord1.lat)
    lon1_rad = math.radians(coord1.lon)
    lat2_rad = math.radians(coord2.lat)
    lon2_rad = math.radians(coord2.lon)

    dlon = lon2_rad - lon1_rad
    y = math.sin(dlon) * math.cos(lat2_rad)
    x = (math.cos(lat1_rad) * math.sin(lat2_rad) -
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))

    bearing_rad = math.atan2(y, x)
    bearing_deg = (math.degrees(bearing_rad) + 360.0) % 360.0
    return bearing_deg


def bearing_to_direction(bearing_deg: float) -> str:
    """Converts a compass bearing in degrees to a 16-wind compass direction name."""
    directions = [
        "North", "North-Northeast", "Northeast", "East-Northeast",
        "East", "East-Southeast", "Southeast", "South-Southeast",
        "South", "South-Southwest", "Southwest", "West-Southwest",
        "West", "West-Northwest", "Northwest", "North-Northwest"
    ]
    idx = int((bearing_deg + 11.25) / 22.5) % 16
    return directions[idx]


def compute_distance(
    origin_name: str,
    origin_coords: GeoCoord,
    dest_name: str,
    dest_coords: GeoCoord
) -> DistanceResult:
    """Computes comprehensive distance, flight time, and geographic bearing between two points."""
    dist_km = haversine_distance_km(origin_coords, dest_coords)
    dist_miles = dist_km * KM_TO_MILES
    bearing = calculate_bearing(origin_coords, dest_coords)
    direction = bearing_to_direction(bearing)

    # Commercial aviation estimation: ~850 km/h cruising speed + 0.5 hr taxi/climb/descent
    flight_hours = (dist_km / 850.0) + 0.5 if dist_km > 100 else (dist_km / 300.0)

    # Road travel approximation (approx 1.25x road curvature factor at ~75 km/h avg)
    # Only applicable if points are connected by land (approximated)
    driving_hours = (dist_km * 1.25) / 75.0 if dist_km < 4000 else None

    context = (
        f"{dest_name} is located {dist_km:,.1f} km ({dist_miles:,.1f} miles) "
        f"{direction.lower()} ({bearing:.1f}°) of {origin_name} as the crow flies."
    )

    return DistanceResult(
        origin_name=origin_name,
        destination_name=dest_name,
        origin_coords=origin_coords,
        destination_coords=dest_coords,
        distance_km=round(dist_km, 2),
        distance_miles=round(dist_miles, 2),
        bearing_degrees=round(bearing, 1),
        compass_direction=direction,
        flight_time_hours=round(flight_hours, 1),
        driving_time_hours=round(driving_hours, 1) if driving_hours else None,
        context=context
    )
