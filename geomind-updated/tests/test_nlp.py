"""
Unit tests for NLP, fuzzy matching, typo handling, and intent extraction.
"""
import unittest
from geomind.core.nlp import NLPEngine, levenshtein_distance, string_similarity
from geomind.core.types import Domain, Intent


class TestNLP(unittest.TestCase):

    def setUp(self):
        self.nlp = NLPEngine()

    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("delhi", "delhi"), 0)
        self.assertEqual(levenshtein_distance("delhi", "delh"), 1)
        # Transposition / insertion
        self.assertEqual(levenshtein_distance("mumbi", "mumbai"), 1)
        self.assertEqual(levenshtein_distance("ditace", "distance"), 2)

    def test_string_similarity(self):
        self.assertAlmostEqual(string_similarity("paris", "paris"), 1.0)
        self.assertGreater(string_similarity("mumbi", "mumbai"), 0.6)
        self.assertGreater(string_similarity("ditace", "distance"), 0.7)

    def test_prompt_typo_example(self):
        """Specifically verifies the prompt requirement: 'ditace between delhi & mumbi' -> 'distance between Delhi and Mumbai'."""
        query = "ditace between delhi & mumbi"
        intent, domain, interpreted, entities = self.nlp.extract_entities_and_intent(query)
        self.assertEqual(intent, Intent.DISTANCE_CALCULATION)
        self.assertEqual(domain, Domain.DISTANCE)
        self.assertEqual(interpreted.lower(), "distance between delhi and mumbai")
        resolved = [e[1] for e in entities]
        self.assertIn("Delhi", resolved)
        self.assertIn("Mumbai", resolved)

    def test_capital_query_with_typo(self):
        query = "captial of fance"
        intent, domain, interpreted, entities = self.nlp.extract_entities_and_intent(query)
        self.assertEqual(intent, Intent.CAPITAL_LOOKUP)
        self.assertEqual(domain, Domain.GEOGRAPHY)
        self.assertIn("France", [e[1] for e in entities])

    def test_comparison_query(self):
        query = "compare india vs china"
        intent, domain, interpreted, entities = self.nlp.extract_entities_and_intent(query)
        self.assertEqual(intent, Intent.COMPARISON)
        self.assertEqual(domain, Domain.COMPARISON)
        self.assertEqual(len(entities), 2)

    def test_causes_consequences_query(self):
        query = "causes and consequences of ww1"
        intent, domain, interpreted, entities = self.nlp.extract_entities_and_intent(query)
        self.assertEqual(intent, Intent.CAUSE_AND_CONSEQUENCE)
        self.assertEqual(domain, Domain.HISTORY)
        self.assertIn("World War I", [e[1] for e in entities])

    def test_concept_definition_query(self):
        query = "define federalism"
        intent, domain, interpreted, entities = self.nlp.extract_entities_and_intent(query)
        self.assertEqual(intent, Intent.DEFINITION)
        self.assertEqual(domain, Domain.SOCIAL_STUDIES)
        self.assertIn("Federalism", [e[1] for e in entities])

    def test_greeting_detection(self):
        for greeting in ("hi", "Hello!", "hey", "yo", "sup", "good morning",
                          "Good Evening", "what's up", "howdy", "hiya"):
            self.assertTrue(self.nlp.is_greeting(greeting), f"Expected '{greeting}' to be a greeting")

    def test_greeting_intent_routing(self):
        for greeting in ("hi", "hello there", "good morning", "yo what's up"):
            intent, domain, interpreted, entities = self.nlp.extract_entities_and_intent(greeting)
            self.assertEqual(intent, Intent.GREETING)
            self.assertEqual(domain, Domain.GENERAL)

    def test_greeting_does_not_hijack_real_questions(self):
        """A longer domain question shouldn't be misread as a greeting."""
        query = "captial of fance"
        intent, domain, interpreted, entities = self.nlp.extract_entities_and_intent(query)
        self.assertNotEqual(intent, Intent.GREETING)


if __name__ == "__main__":
    unittest.main()
