"""
Unit tests for Geography knowledge source (countries, capitals, cities, borders, currencies).
"""
import unittest
from geomind.knowledge.geography import GeographyKnowledgeSource
from geomind.core.types import Intent


class TestGeography(unittest.TestCase):

    def setUp(self):
        self.geo = GeographyKnowledgeSource()

    def test_capital_lookup(self):
        res = self.geo.query(Intent.CAPITAL_LOOKUP, ["france"], "capital of france")
        self.assertIsNotNone(res)
        self.assertIn("Paris", res.text)
        self.assertIn("France", res.text)

    def test_capital_india(self):
        res = self.geo.query(Intent.CAPITAL_LOOKUP, ["india"], "capital of india")
        self.assertIsNotNone(res)
        self.assertIn("New Delhi", res.text)

    def test_country_profile(self):
        res = self.geo.query(Intent.COUNTRY_INFO, ["japan"], "tell me about japan")
        self.assertIsNotNone(res)
        self.assertIn("Tokyo", res.text)
        self.assertIn("Yen", res.text)

    def test_bordering_countries(self):
        res = self.geo.query(Intent.BORDERING_COUNTRIES, ["germany"], "borders of germany")
        self.assertIsNotNone(res)
        self.assertIn("France", res.text)
        self.assertIn("Poland", res.text)

    def test_currency_lookup(self):
        res = self.geo.query(Intent.CURRENCY_LOOKUP, ["india"], "currency of india")
        self.assertIsNotNone(res)
        self.assertIn("Rupee", res.text)

    def test_city_resolution(self):
        res = self.geo.resolve_location("mumbai")
        self.assertIsNotNone(res)
        name, coords, data = res
        self.assertEqual(name, "Mumbai")
        self.assertAlmostEqual(coords.lat, 19.0760, places=2)


if __name__ == "__main__":
    unittest.main()
