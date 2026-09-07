"""
Unit tests for geodesic distance calculation, bearings, and route approximations.
"""
import unittest
from geomind.core.types import GeoCoord
from geomind.knowledge.distance import (
    haversine_distance_km,
    calculate_bearing,
    bearing_to_direction,
    compute_distance
)


class TestDistance(unittest.TestCase):

    def test_haversine_delhi_to_mumbai(self):
        # Delhi: ~28.6139° N, 77.2090° E
        # Mumbai: ~19.0760° N, 72.8777° E
        delhi = GeoCoord(28.6139, 77.2090)
        mumbai = GeoCoord(19.0760, 72.8777)
        dist_km = haversine_distance_km(delhi, mumbai)

        # Expected great-circle distance is approx 1,148 km
        self.assertAlmostEqual(dist_km, 1148.0, delta=20.0)

    def test_haversine_same_point(self):
        pt = GeoCoord(51.5074, -0.1278)
        self.assertEqual(haversine_distance_km(pt, pt), 0.0)

    def test_bearing_calculation(self):
        delhi = GeoCoord(28.6139, 77.2090)
        mumbai = GeoCoord(19.0760, 72.8777)
        bearing = calculate_bearing(delhi, mumbai)
        direction = bearing_to_direction(bearing)

        # Bearing from Delhi down to Mumbai is approx ~201° (South-Southwest)
        self.assertGreater(bearing, 190.0)
        self.assertLess(bearing, 215.0)
        self.assertIn("South", direction)

    def test_compute_distance_full(self):
        london = GeoCoord(51.5074, -0.1278)
        paris = GeoCoord(48.8566, 2.3522)
        res = compute_distance("London", london, "Paris", paris)

        self.assertGreater(res.distance_km, 300)
        self.assertLess(res.distance_km, 400)
        self.assertGreater(res.distance_miles, 200)
        self.assertIsNotNone(res.flight_time_hours)
        self.assertIn("London", res.context)
        self.assertIn("Paris", res.context)


if __name__ == "__main__":
    unittest.main()
