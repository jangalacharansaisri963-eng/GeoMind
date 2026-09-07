"""
Tests for the optional Playwright-backed web research fallback.

These tests deliberately don't require Playwright/a browser to be installed —
is_available() must degrade gracefully to False in that case, and research()
must return None rather than raising.
"""
import unittest
from geomind.knowledge.web_research import WebResearchEngine


class TestWebResearchEngine(unittest.TestCase):

    def test_disabled_engine_is_never_available(self):
        engine = WebResearchEngine(enabled=False)
        self.assertFalse(engine.is_available())

    def test_disabled_engine_research_returns_none(self):
        engine = WebResearchEngine(enabled=False)
        self.assertIsNone(engine.research("population of Nairobi"))

    def test_is_available_never_raises(self):
        """Whether or not Playwright/a browser is installed in this environment,
        checking availability must not throw."""
        engine = WebResearchEngine()
        try:
            engine.is_available()
        except Exception as e:  # pragma: no cover - failure would be the bug
            self.fail(f"is_available() raised unexpectedly: {e}")

    def test_research_returns_none_when_unavailable(self):
        engine = WebResearchEngine()
        engine._checked_browser = True
        engine._browser_ok = False
        self.assertIsNone(engine.research("anything"))


if __name__ == "__main__":
    unittest.main()
