"""
CI smoke test for the Playwright-backed web research fallback
(geomind/knowledge/web_research.py).

This runs on a normal GitHub Actions Ubuntu runner (not Termux/mobile, where
Playwright's browser binaries generally can't be installed) after:

    pip install "geomind-ai[research]"
    python -m playwright install --with-deps chromium

It's informational, not a hard requirement of the training job — network
flakiness or search-engine markup changes shouldn't fail the whole CI run,
so failures here are logged clearly but exit 0.

Usage:
    python scripts/research_check.py "capital of Kenya"
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from geomind.knowledge.web_research import WebResearchEngine  # noqa: E402


def main() -> None:
    query = sys.argv[1] if len(sys.argv) > 1 else "current population of Nairobi"
    engine = WebResearchEngine()

    if not engine.is_available():
        print("⚠️  Web research engine unavailable (Playwright/Chromium not installed, or no network).")
        print("    This is expected on machines without `playwright install chromium` — not a failure.")
        return

    result = engine.research(query)
    if result is None:
        print(f"⚠️  Live search for {query!r} returned no results (network hiccup or markup change).")
        return

    print(f"✅ Live web research OK for query: {query!r}")
    print(result.text)
    print("Sources:", result.sources)


if __name__ == "__main__":
    main()
