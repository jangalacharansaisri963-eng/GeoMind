"""
Unit tests for History knowledge base (events, figures, causes, consequences).
"""
import unittest
from geomind.knowledge.history import HistoryKnowledgeSource
from geomind.core.types import Intent


class TestHistory(unittest.TestCase):

    def setUp(self):
        self.hist = HistoryKnowledgeSource()

    def test_causes_consequences_ww1(self):
        res = self.hist.query(Intent.CAUSE_AND_CONSEQUENCE, ["world war 1"], "causes of world war 1")
        self.assertIsNotNone(res)
        self.assertIn("Versailles", res.text)
        self.assertIn("Franz Ferdinand", res.text)
        self.assertIn("Militarism", res.text)

    def test_french_revolution(self):
        res = self.hist.query(Intent.HISTORICAL_EVENT, ["french revolution"], "about french revolution")
        self.assertIsNotNone(res)
        self.assertIn("1789", res.text)
        self.assertTrue("Bastille" in res.text or "Louis XVI" in res.text)

    def test_historical_figure_napoleon(self):
        res = self.hist.query(Intent.HISTORICAL_FIGURE, ["napoleon bonaparte"], "who was napoleon")
        self.assertIsNotNone(res)
        self.assertIn("Napoleonic Code", res.text)
        self.assertIn("Waterloo", res.text)

    def test_historical_figure_gandhi(self):
        res = self.hist.query(Intent.HISTORICAL_FIGURE, ["mahatma gandhi"], "who was gandhi")
        self.assertIsNotNone(res)
        self.assertIn("Satyagraha", res.text)
        self.assertIn("1947", res.text)


if __name__ == "__main__":
    unittest.main()
