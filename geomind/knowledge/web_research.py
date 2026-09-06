"""
Live web research fallback for GeoMind.

GeoMind answers primarily from its own curated Geography/History/Social Studies
datasets (see geomind/data/). When a question doesn't match anything in that
local knowledge base, this module can optionally use Playwright to drive a
real, unmodified Chromium/Firefox browser, run a web search, and pull back a
short summary with source links — the same thing a person would do by hand,
just automated.

This is intentionally NOT a "custom/overpowered browser build". It uses
Playwright (https://playwright.dev/python/), the standard, official browser
automation library, purely to load pages and read their text.

Playwright is an optional dependency. If it isn't installed, or no browser
has been provisioned (`playwright install chromium`), or there's no network
access, `is_available()` returns False and GeoMind simply falls back to its
normal "I don't know that one" response — it never crashes the app.
"""
import re
from dataclasses import dataclass, field
from typing import List, Optional

try:
    from playwright.sync_api import sync_playwright
    _PLAYWRIGHT_IMPORT_OK = True
except ImportError:
    _PLAYWRIGHT_IMPORT_OK = False


SEARCH_URL = "https://html.duckduckgo.com/html/?q={query}"
DEFAULT_TIMEOUT_MS = 8000
MAX_SNIPPET_CHARS = 320


@dataclass
class WebResearchResult:
    """A short synthesized answer plus the pages it came from."""
    text: str
    sources: List[str] = field(default_factory=list)


class WebResearchEngine:
    """
    Optional live-search fallback. Launches a real browser via Playwright,
    searches the web, and reads back the top results' text.

    Usage:
        engine = WebResearchEngine()
        if engine.is_available():
            result = engine.research("current population of Nairobi 2026")
    """

    def __init__(self, headless: bool = True, max_results: int = 3, enabled: bool = True):
        self.headless = headless
        self.max_results = max_results
        self.enabled = enabled
        self._checked_browser = False
        self._browser_ok = False

    def is_available(self) -> bool:
        """
        Cheap, safe check for whether live research can run at all.
        Never raises — just reports False on any missing piece.
        """
        if not self.enabled or not _PLAYWRIGHT_IMPORT_OK:
            return False
        if self._checked_browser:
            return self._browser_ok
        self._checked_browser = True
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                browser.close()
            self._browser_ok = True
        except Exception:
            # No browser binaries installed (needs `playwright install chromium`),
            # sandboxed environment, no network, etc.
            self._browser_ok = False
        return self._browser_ok

    def research(self, query: str) -> Optional[WebResearchResult]:
        """
        Searches the web for `query` using a real browser and returns a short
        synthesized summary with source URLs. Returns None on any failure so
        callers can cleanly fall back to the local knowledge base.
        """
        if not self.is_available():
            return None

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.set_default_timeout(DEFAULT_TIMEOUT_MS)
                page.goto(SEARCH_URL.format(query=query.replace(" ", "+")))

                results = page.query_selector_all(".result")
                snippets: List[str] = []
                sources: List[str] = []

                for result in results[: self.max_results]:
                    title_el = result.query_selector(".result__title a")
                    snippet_el = result.query_selector(".result__snippet")
                    if not title_el:
                        continue

                    url = title_el.get_attribute("href") or ""
                    snippet_text = snippet_el.inner_text().strip() if snippet_el else ""

                    if snippet_text:
                        snippets.append(_truncate(snippet_text, MAX_SNIPPET_CHARS))
                    if url:
                        sources.append(url)

                browser.close()

                if not snippets:
                    return None

                summary = "🔎 **Live Web Research**\n\n" + "\n\n".join(
                    f"- {s}" for s in snippets
                )
                return WebResearchResult(text=summary, sources=sources or ["Web search"])

        except Exception:
            return None


def _truncate(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rsplit(" ", 1)[0] + "…"
