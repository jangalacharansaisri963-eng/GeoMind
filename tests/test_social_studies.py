"""
Unit tests for Social Studies knowledge source (civics, economics, definitions, governance).
"""
import unittest
from geomind.knowledge.social_studies import SocialStudiesKnowledgeSource
from geomind.core.types import Intent


class TestSocialStudies(unittest.TestCase):

    def setUp(self):
        self.soc = SocialStudiesKnowledgeSource()

    def test_democracy_definition(self):
        res = self.soc.query(Intent.DEFINITION, ["democracy"], "what is democracy")
        self.assertIsNotNone(res)
        self.assertIn("Democracy", res.text)
        self.assertIn("elections", res.text.lower())

    def test_federalism_definition(self):
        res = self.soc.query(Intent.DEFINITION, ["federalism"], "define federalism")
        self.assertIsNotNone(res)
        self.assertIn("Federalism", res.text)
        self.assertIn("constitution", res.text.lower())

    def test_capitalism_definition(self):
        res = self.soc.query(Intent.DEFINITION, ["capitalism"], "explain capitalism")
        self.assertIsNotNone(res)
        self.assertIn("Capitalism", res.text)
        self.assertIn("private property", res.text.lower())

    def test_separation_of_powers(self):
        res = self.soc.query(Intent.DEFINITION, ["separation of powers"], "what is separation of powers")
        self.assertIsNotNone(res)
        self.assertIn("Legislative", res.text)
        self.assertIn("Executive", res.text)
        self.assertIn("Judicial", res.text)


if __name__ == "__main__":
    unittest.main()
