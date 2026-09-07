"""
Unit tests for the Comparison Engine.
"""
import unittest
from geomind.knowledge.comparison import ComparisonEngine
from geomind.core.types import Intent, Domain


class TestComparison(unittest.TestCase):

    def setUp(self):
        self.comp = ComparisonEngine()

    def test_compare_countries(self):
        res = self.comp.query(Intent.COMPARISON, ["india", "china"], "compare india and china")
        self.assertIsNotNone(res)
        self.assertEqual(res.domain, Domain.COMPARISON)
        self.assertIn("India", res.text)
        self.assertIn("China", res.text)
        self.assertIn("Population", res.text)

    def test_compare_cities(self):
        res = self.comp.query(Intent.COMPARISON, ["delhi", "mumbai"], "compare delhi vs mumbai")
        self.assertIsNotNone(res)
        self.assertIn("Delhi", res.text)
        self.assertIn("Mumbai", res.text)

    def test_compare_wars(self):
        res = self.comp.query(Intent.COMPARISON, ["world war 1", "world war 2"], "compare ww1 and ww2")
        self.assertIsNotNone(res)
        self.assertIn("World War I", res.text)
        self.assertIn("World War II", res.text)


if __name__ == "__main__":
    unittest.main()
