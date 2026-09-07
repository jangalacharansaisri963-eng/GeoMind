"""
Integration and API tests for GeoMind agent and ChatSession.
"""
import os
import tempfile
import unittest
from geomind.core.agent import GeoMind
from geomind.core.types import Domain, Intent


class TestGeoMindAgent(unittest.TestCase):

    def setUp(self):
        # Initialize standard GeoMind agent with GeoMind-1 model
        self.ai = GeoMind()

    def test_ask_typo_distance(self):
        """Verify prompt requirement: 'ditace between delhi & mumbi'."""
        res = self.ai.ask("ditace between delhi & mumbi")
        self.assertEqual(res.domain, Domain.DISTANCE)
        self.assertEqual(res.interpreted_query.lower(), "distance between delhi and mumbai")
        self.assertIn("1,148", res.text)
        self.assertIn("Mumbai", res.text)

    def test_direct_distance_method(self):
        dist = self.ai.distance("Delhi", "Mumbai")
        self.assertIsNotNone(dist)
        self.assertAlmostEqual(dist.distance_km, 1148.0, delta=20.0)

    def test_capital_method(self):
        cap = self.ai.capital_of("Japan")
        self.assertEqual(cap, "Tokyo")

    def test_country_method(self):
        info = self.ai.country("India")
        self.assertIsNotNone(info)
        self.assertEqual(info["capital"], "New Delhi")

    def test_greeting_response(self):
        for greeting in ("hi", "hello", "yo", "good morning", "what's up"):
            res = self.ai.ask(greeting)
            self.assertEqual(res.intent, Intent.GREETING)
            self.assertEqual(res.domain, Domain.GENERAL)
            self.assertTrue(len(res.text) > 0)

    def test_multi_turn_chat_session(self):
        chat = self.ai.start_chat()
        reply1 = chat.send("Tell me about the French Revolution")
        self.assertIn("French Revolution", reply1.text)

        # Multi-turn anaphoric follow-up
        reply2 = chat.send("What were its causes?")
        self.assertIn("Causes", reply2.text) or self.assertIn("Estate", reply2.text)

        self.assertEqual(len(chat.history), 4)  # 2 user + 2 assistant messages

    def test_session_export(self):
        chat = self.ai.start_chat()
        chat.send("capital of france")
        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = os.path.join(tmpdir, "session.md")
            json_path = os.path.join(tmpdir, "session.json")
            chat.export_markdown(md_path)
            chat.export_json(json_path)

            self.assertTrue(os.path.exists(md_path))
            self.assertTrue(os.path.exists(json_path))
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertIn("capital of france", content)


if __name__ == "__main__":
    unittest.main()
