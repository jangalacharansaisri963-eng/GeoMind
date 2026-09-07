"""
Live web research fallback for GeoMind.

GeoMind answers primarily from its own curated Geography/History/Social
Studies datasets (see geomind/knowledge/*.py and geomind/data/). When a
question doesn't match anything in that local knowledge base, this module
can optionally reach out to the web for an answer.

Two independent backends are supported, tried in this order:

1. **Google Programmable Search (Custom Search JSON API)** — the primary,
   recommended path. It's a plain HTTPS GET request built with Python's
   standard library only (`urllib`), so it needs no extra pip install and
   works everywhere GeoMind runs, including Termux/Android, where browser
   automation tools cannot install. Configure it with two environment
   variables:

       GOOGLE_API_KEY            (from Google Cloud Console)
       GOOGLE_SEARCH_ENGINE_ID   (the "cx" value from
                                  https://programmablesearchengine.google.com)

   `GOOGLE_SEARCH_API_KEY` and `GOOGLE_CSE_ID` are accepted as aliases for
   the two variables above, in case that's what you already set.

2. **Playwright (optional, secondary)** — if Google Search isn't configured
   but the `playwright` package *and* a Chromium binary are installed
   (`pip install "geomind-ai[research]"` then
   `python -m playwright install chromium`), GeoMind will fall back to
   driving a real, unmodified browser instead. This only works on standard
   glibc-based Linux/macOS/Windows (e.g. a laptop or a CI runner) — not on
   Termux, since Android's Bionic libc can't run Playwright's browser
   binaries.

If neither backend is configured/available, `is_available()` returns
`False` and GeoMind simply falls back to its normal offline response —
this module never raises out to the caller.
"""
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import List, Optional

try:
    from playwright.sync_api import sync_playwright
    _PLAYWRIGHT_IMPORT_OK = True
except ImportError:
    _PLAYWRIGHT_IMPORT_OK = False


GOOGLE_SEARCH_ENDPOINT = "https://www.googleapis.com/customsearch/v1"
DUCKDUCKGO_SEARCH_URL = "https://html.duckduckgo.com/html/?q={query}"
REQUEST_TIMEOUT_SECS = 8
DEFAULT_TIMEOUT_MS = 8000
MAX_RESULTS = 3
MAX_SNIPPET_CHARS = 320


@dataclass
class WebResearchResult:
    """A short synthesized answer plus the pages it came from."""
    text: str
    sources: List[str] = field(default_factory=list)


class WebResearchEngine:
    """
    Optional live-search fallback for questions outside GeoMind's local
    datasets. Tries Google Programmable Search first (stdlib HTTP, works
    everywhere including Termux), then falls back to Playwright browser
    automation if that's installed and Google Search isn't configured.

    Usage:
        engine = WebResearchEngine()
        if engine.is_available():
            result = engine.research("current population of Nairobi 2026")
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        search_engine_id: Optional[str] = None,
        enabled: bool = True,
        max_results: int = MAX_RESULTS,
        use_playwright_fallback: bool = True,
        headless: bool = True,
    ):
        self.enabled = enabled
        self.max_results = max_results
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_SEARCH_API_KEY")
        self.search_engine_id = (
            search_engine_id
            or os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
            or os.environ.get("GOOGLE_CSE_ID")
        )
        self.use_playwright_fallback = use_playwright_fallback
        self.headless = headless
        self._checked_browser = False
        self._browser_ok = False

    # ------------------------------------------------------------------
    # Availability checks
    # ------------------------------------------------------------------

    def _google_configured(self) -> bool:
        return bool(self.enabled and self.api_key and self.search_engine_id)

    def _playwright_available(self) -> bool:
        """
        Cheap, safe check for whether the Playwright fallback can run at
        all. Never raises — just reports False on any missing piece.
        """
        if not self.enabled or not self.use_playwright_fallback or not _PLAYWRIGHT_IMPORT_OK:
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
            # No browser binaries installed (needs `playwright install
            # chromium`), sandboxed environment, no network, etc.
            self._browser_ok = False
        return self._browser_ok

    def is_available(self) -> bool:
        """True if either backend is usable right now."""
        return self._google_configured() or self._playwright_available()

    # ------------------------------------------------------------------
    # Research
    # ------------------------------------------------------------------

    def research(self, query: str) -> Optional[WebResearchResult]:
        """
        Searches the web for `query` and returns a short synthesized
        summary with source URLs. Returns None on any failure (bad
        config, network issue, no results) so callers can cleanly fall
        back to the local knowledge base.
        """
        if not self.enabled:
            return None

        if self._google_configured():
            result = self._research_via_google(query)
            if result is not None:
                return result
            # Fall through to Playwright if Google's request failed for
            # some reason (quota exceeded, network hiccup, etc.)

        if self._playwright_available():
            return self._research_via_playwright(query)

        return None

    def _research_via_google(self, query: str) -> Optional[WebResearchResult]:
        params = {
            "key": self.api_key,
            "cx": self.search_engine_id,
            "q": query,
            "num": self.max_results,
        }
        url = f"{GOOGLE_SEARCH_ENDPOINT}?{urllib.parse.urlencode(params)}"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "GeoMind/1.0"})
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECS) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
            return None
        except Exception:
            return None

        items = data.get("items") or []
        if not items:
            return None

        snippets: List[str] = []
        sources: List[str] = []
        for item in items[: self.max_results]:
            snippet = (item.get("snippet") or "").strip()
            link = item.get("link") or ""
            title = (item.get("title") or "").strip()
            if snippet:
                label = f"**{title}**: {snippet}" if title else snippet
                snippets.append(_truncate(label, MAX_SNIPPET_CHARS))
            if link:
                sources.append(link)

        if not snippets:
            return None

        summary = "🔎 **Live Web Research (Google Search)**\n\n" + "\n\n".join(f"- {s}" for s in snippets)
        return WebResearchResult(text=summary, sources=sources or ["Google Search"])

    def _research_via_playwright(self, query: str) -> Optional[WebResearchResult]:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                page.set_default_timeout(DEFAULT_TIMEOUT_MS)
                page.goto(DUCKDUCKGO_SEARCH_URL.format(query=urllib.parse.quote_plus(query)))

                results = page.query_selector_all(".result")
                snippets: List[str] = []
                sources: List[str] = []

                for result in results[: self.max_results]:
                    title_el = result.query_selector(".result__title a")
                    snippet_el = result.query_selector(".result__snippet")
                    if not title_el:
                        continue

                    link = title_el.get_attribute("href") or ""
                    snippet_text = snippet_el.inner_text().strip() if snippet_el else ""

                    if snippet_text:
                        snippets.append(_truncate(snippet_text, MAX_SNIPPET_CHARS))
                    if link:
                        sources.append(link)

                browser.close()

                if not snippets:
                    return None

                summary = "🔎 **Live Web Research (Browser Search)**\n\n" + "\n\n".join(f"- {s}" for s in snippets)
                return WebResearchResult(text=summary, sources=sources or ["Web search"])

        except Exception:
            return None


def _truncate(text: str, max_chars: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rsplit(" ", 1)[0] + "…"
