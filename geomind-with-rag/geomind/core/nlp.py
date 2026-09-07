"""
Natural Language Processing, Fuzzy Matching, Spelling Correction, and Intent Parsing.
"""
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from geomind.core.types import Domain, Intent
from geomind.knowledge.geography import COUNTRIES_DATA, WORLD_CITIES
from geomind.knowledge.history import HISTORICAL_EVENTS, HISTORICAL_FIGURES
from geomind.knowledge.social_studies import SOCIAL_STUDIES_CONCEPTS


def levenshtein_distance(s1: str, s2: str) -> int:
    """Computes the Levenshtein distance between two strings with transposition (Damerau-Levenshtein)."""
    d: Dict[Tuple[int, int], int] = {}
    len1, len2 = len(s1), len(s2)

    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len1):
        for j in range(len2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,        # deletion
                d[(i, j - 1)] + 1,        # insertion
                d[(i - 1, j - 1)] + cost  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition

    return d[(len1 - 1, len2 - 1)]


def string_similarity(s1: str, s2: str) -> float:
    """Returns a normalized similarity score between 0.0 and 1.0."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    s1, s2 = s1.lower().strip(), s2.lower().strip()
    if s1 == s2:
        return 1.0
    dist = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return max(0.0, 1.0 - (dist / max_len))


# Domain vocabulary mappings for common typos and abbreviations
COMMON_CORRECTIONS: Dict[str, str] = {
    # Distance terms
    "ditace": "distance",
    "ditanc": "distance",
    "distnce": "distance",
    "dstance": "distance",
    "distanc": "distance",
    "dist": "distance",
    "betwen": "between",
    "btwn": "between",
    "beween": "between",
    "betweeen": "between",
    "bet": "between",
    # Capital terms
    "captial": "capital",
    "captal": "capital",
    "capitl": "capital",
    "capitol": "capital",
    # Compare terms
    "compar": "compare",
    "compair": "compare",
    "differnce": "difference",
    "diff": "difference",
    "diffrence": "difference",
    # Population terms
    "populaton": "population",
    "populatn": "population",
    "pop": "population",
    # History terms
    "histroy": "history",
    "revoluton": "revolution",
    "revelution": "revolution",
    "consequens": "consequences",
    "consequence": "consequences",
    "consequnces": "consequences",
    "caus": "causes",
    "cuases": "causes",
    # Definition terms
    "defin": "define",
    "deffinition": "definition",
    "defination": "definition",
    # Informal words
    "whos": "who was",
    "whats": "what is",
    "wher": "where",
    "whr": "where",
    "howfar": "how far",
    "plz": "please",
    "pls": "please"
}

COMMON_ABBREVIATIONS: Dict[str, str] = {
    "&": "and",
    "vs": "versus",
    "vs.": "versus",
    "v": "versus",
    "v.": "versus",
    "del": "delhi",
    "bom": "mumbai",
    "nyc": "new york",
    "la": "los angeles",
    "dc": "washington dc",
    "usa": "united states",
    "us": "united states",
    "uk": "united kingdom",
    "uae": "united arab emirates",
    "ussr": "soviet union",
    "drc": "democratic republic of the congo",
    "ww1": "world war 1",
    "wwi": "world war 1",
    "ww2": "world war 2",
    "wwii": "world war 2"
}


# Casual conversational openers that should short-circuit straight to a greeting
# response instead of being parsed as a domain question.
GREETING_PATTERNS = [
    r"^(hi+|hello+|hey+|yo+|sup|howdy|hiya|greetings)\b",
    r"^(good\s*morning|good\s*afternoon|good\s*evening|good\s*day)\b",
    r"\bwhat'?s?\s*up\b",
    r"^how\s*(are|r)\s*(you|u)\b",
    r"^(what'?s\s+good|yo+\s+what'?s\s+up)\b",
]
GREETING_REGEX = re.compile("|".join(f"(?:{p})" for p in GREETING_PATTERNS), re.IGNORECASE)


class NLPEngine:
    """Parses, normalizes, corrects typos, and extracts entities and intent from queries."""

    def __init__(self):
        self._build_entity_index()

    def is_greeting(self, text: str) -> bool:
        """Detects casual conversational openers (hi, hello, good morning, what's up, etc.)."""
        candidate = text.strip().lower()
        if not candidate:
            return False
        # Keep this narrow: only short messages count as greetings, so a longer
        # question that happens to start with "hi" (rare) doesn't get hijacked.
        if len(candidate.split()) > 6:
            return False
        return bool(GREETING_REGEX.search(candidate))

    def _build_entity_index(self):
        """Constructs an exhaustive lookup index of cities, countries, events, figures, and concepts."""
        self.entity_index: Dict[str, Tuple[str, str]] = {}  # lower_term -> (canonical_name, category)

        # 1. Cities
        for key, data in WORLD_CITIES.items():
            self.entity_index[key] = (data["name"], "city")
            self.entity_index[data["name"].lower()] = (data["name"], "city")

        # 2. Countries
        for key, data in COUNTRIES_DATA.items():
            self.entity_index[key] = (data["name"], "country")
            self.entity_index[data["name"].lower()] = (data["name"], "country")

        # 3. Historical Events
        for key, data in HISTORICAL_EVENTS.items():
            self.entity_index[key] = (data["title"], "event")
            for alias in data.get("aliases", []):
                self.entity_index[alias.lower()] = (data["title"], "event")

        # 4. Historical Figures
        for key, data in HISTORICAL_FIGURES.items():
            self.entity_index[key] = (data["name"], "figure")
            for alias in data.get("aliases", []):
                self.entity_index[alias.lower()] = (data["name"], "figure")

        # 5. Social Studies Concepts
        for key, data in SOCIAL_STUDIES_CONCEPTS.items():
            self.entity_index[key] = (data["term"], "concept")
            for alias in data.get("aliases", []):
                self.entity_index[alias.lower()] = (data["term"], "concept")

        # 6. Expanded Wikipedia Datasets (Mountains, Rivers, Oceans, Deserts, Lakes, Islands, Landmarks, Straits, Eras, Figures, Orgs)
        import os, json
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        if os.path.exists(data_dir):
            def load_json_records(fname: str) -> List[Dict[str, Any]]:
                fp = os.path.join(data_dir, fname)
                if os.path.exists(fp):
                    try:
                        with open(fp, "r", encoding="utf-8") as f:
                            return json.load(f)
                    except Exception:
                        return []
                return []

            for m in load_json_records("mountains.json"):
                name = m.get("name", "")
                self.entity_index[name.lower()] = (name, "mountain")
                for alias in m.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "mountain")

            for r in load_json_records("rivers.json"):
                name = r.get("name", "")
                self.entity_index[name.lower()] = (name, "river")
                for alias in r.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "river")

            for o in load_json_records("oceans_seas.json"):
                name = o.get("name", "")
                self.entity_index[name.lower()] = (name, "ocean")
                for alias in o.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "ocean")

            for d in load_json_records("deserts.json"):
                name = d.get("name", "")
                self.entity_index[name.lower()] = (name, "desert")
                for alias in d.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "desert")

            for isl in load_json_records("islands.json"):
                name = isl.get("name", "")
                self.entity_index[name.lower()] = (name, "island")

            for lk in load_json_records("lakes.json"):
                name = lk.get("name", "")
                self.entity_index[name.lower()] = (name, "lake")
                for alias in lk.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "lake")

            for w in load_json_records("world_wonders_landmarks.json"):
                name = w.get("name", "")
                self.entity_index[name.lower()] = (name, "landmark")
                for alias in w.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "landmark")

            for st in load_json_records("straits_and_canals.json"):
                name = st.get("name", "")
                self.entity_index[name.lower()] = (name, "strait")
                for alias in st.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "strait")

            for er in load_json_records("historical_eras.json"):
                name = er.get("name", "")
                self.entity_index[name.lower()] = (name, "era")
                for alias in er.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "era")

            for fig in load_json_records("historical_figures.json"):
                name = fig.get("name", "")
                self.entity_index[name.lower()] = (name, "figure")
                for alias in fig.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "figure")

            for gov in load_json_records("forms_of_government.json"):
                name = gov.get("name", "")
                self.entity_index[name.lower()] = (name, "concept")

            for ec in load_json_records("economic_systems.json"):
                name = ec.get("name", "")
                self.entity_index[name.lower()] = (name, "concept")

            for org in load_json_records("international_organizations.json"):
                name = org.get("name", "")
                self.entity_index[name.lower()] = (name, "organization")
                for alias in org.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "organization")

            for cp in load_json_records("constitutional_principles.json"):
                name = cp.get("name", "")
                self.entity_index[name.lower()] = (name, "concept")

            for c in load_json_records("world_countries_encyclopedia.json"):
                name = c.get("name", "")
                self.entity_index[name.lower()] = (name, "country")
                for alias in c.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "country")

            for ci in load_json_records("world_cities_encyclopedia.json"):
                name = ci.get("name", "")
                self.entity_index[name.lower()] = (name, "city")
                for alias in ci.get("aliases", []):
                    self.entity_index[alias.lower()] = (name, "city")

    def normalize_tokens(self, text: str) -> List[str]:
        """Cleans, normalizes abbreviations, and corrects spelling in tokens."""
        # Replace punctuation except for alphanumeric and spaces
        cleaned = re.sub(r"[^\w\s&]", " ", text.lower())
        tokens = cleaned.split()
        normalized: List[str] = []

        for t in tokens:
            # Check abbreviations
            if t in COMMON_ABBREVIATIONS:
                normalized.append(COMMON_ABBREVIATIONS[t])
            # Check typo corrections
            elif t in COMMON_CORRECTIONS:
                normalized.append(COMMON_CORRECTIONS[t])
            else:
                normalized.append(t)

        return normalized

    def fuzzy_match_entity(self, candidate: str, threshold: float = 0.78) -> Optional[Tuple[str, str, float]]:
        """Fuzzy matches a text snippet against the known entity index."""
        candidate = candidate.strip().lower()
        if not candidate:
            return None

        # Exact match
        if candidate in self.entity_index:
            canonical, category = self.entity_index[candidate]
            return (canonical, category, 1.0)

        best_match: Optional[Tuple[str, str, float]] = None
        best_score = 0.0

        for key, (canonical, category) in self.entity_index.items():
            # Quick length check filter
            if abs(len(key) - len(candidate)) > 4 and len(candidate) < 6:
                continue

            score = string_similarity(candidate, key)
            if score > best_score and score >= threshold:
                best_score = score
                best_match = (canonical, category, score)

        return best_match

    def extract_entities_and_intent(self, text: str) -> Tuple[Intent, Domain, str, List[Tuple[str, str]]]:
        """
        Main NLP pipeline: Extracts intent, domain, resolved canonical entities,
        and constructs an accurate interpreted query.
        """
        raw_lower = text.strip().lower()
        tokens = self.normalize_tokens(text)
        normalized_str = " ".join(tokens)

        # 0. Greetings / casual small talk (e.g. "hi", "hello", "good morning", "what's up")
        if self.is_greeting(raw_lower):
            return (
                Intent.GREETING,
                Domain.GENERAL,
                text.strip(),
                []
            )

        # 1. Distance Queries (e.g. "ditace between delhi & mumbi", "distance from london to paris")
        distance_regex = re.compile(
            r"(?:distance|how\s+far|far)\s+(?:between|from)?\s*([a-zA-Z\s]+?)\s+(?:and|&|to)\s+([a-zA-Z\s]+)",
            re.IGNORECASE
        )
        dist_match = distance_regex.search(normalized_str)

        # Fallback distance pattern: "between X and Y"
        if not dist_match and ("distance" in normalized_str or "how far" in normalized_str or "between" in normalized_str):
            between_match = re.search(r"between\s+([a-zA-Z\s]+?)\s+(?:and|&|to)\s+([a-zA-Z\s]+)", normalized_str)
            if between_match:
                dist_match = between_match

        if dist_match:
            loc1_raw = dist_match.group(1).strip()
            loc2_raw = dist_match.group(2).strip()

            match1 = self.fuzzy_match_entity(loc1_raw)
            match2 = self.fuzzy_match_entity(loc2_raw)

            if match1 and match2:
                name1 = match1[0]
                name2 = match2[0]
                interpreted = f"distance between {name1} and {name2}"
                return (
                    Intent.DISTANCE_CALCULATION,
                    Domain.DISTANCE,
                    interpreted,
                    [(loc1_raw, name1), (loc2_raw, name2)]
                )

        # 2. Capital Queries (e.g. "what is the capital of France", "capital of india", "captial of japan")
        capital_regex = re.compile(
            r"(?:capital|captial|captal|seat\s+of\s+government)\s+(?:of|for)?\s*([a-zA-Z\s]+)",
            re.IGNORECASE
        )
        cap_match = capital_regex.search(normalized_str)
        if cap_match:
            country_raw = cap_match.group(1).strip()
            match = self.fuzzy_match_entity(country_raw)
            if match and match[1] == "country":
                canonical = match[0]
                interpreted = f"capital of {canonical}"
                return (
                    Intent.CAPITAL_LOOKUP,
                    Domain.GEOGRAPHY,
                    interpreted,
                    [(country_raw, canonical)]
                )

        # 3. Comparison Queries (e.g. "compare India and China", "Athens vs Sparta", "capitalism vs socialism")
        compare_regex = re.compile(
            r"(?:compare|comparison|versus|difference\s+between)\s+([a-zA-Z0-9\s]+?)\s+(?:and|&|vs|versus|to)\s+([a-zA-Z0-9\s]+)",
            re.IGNORECASE
        )
        comp_match = compare_regex.search(normalized_str)
        if comp_match:
            item1_raw = comp_match.group(1).strip()
            item2_raw = comp_match.group(2).strip()
            m1 = self.fuzzy_match_entity(item1_raw)
            m2 = self.fuzzy_match_entity(item2_raw)

            if m1 and m2:
                interpreted = f"comparison between {m1[0]} and {m2[0]}"
                return (
                    Intent.COMPARISON,
                    Domain.COMPARISON,
                    interpreted,
                    [(item1_raw, m1[0]), (item2_raw, m2[0])]
                )

        # 4. Causes and Consequences of Historical Events
        causes_conseq_regex = re.compile(
            r"(?:causes?\s+and\s+consequences?|causes?\s+&\s+consequences?|causes?|consequences?|effects?|reasons?|aftermath|impact|why\s+did)\s+(?:of|for|behind)?\s*(?:the\s+)?([a-zA-Z0-9\s]+)",
            re.IGNORECASE
        )
        cc_match = causes_conseq_regex.search(normalized_str)
        if cc_match:
            event_raw = cc_match.group(1).strip()
            # Strip trailing words like 'happen' or 'start' if any
            event_raw = re.sub(r"\s+(?:happen|occur|start|begin)$", "", event_raw)
            m = self.fuzzy_match_entity(event_raw)
            if m and m[1] == "event":
                interpreted = f"causes and consequences of {m[0]}"
                return (
                    Intent.CAUSE_AND_CONSEQUENCE,
                    Domain.HISTORY,
                    interpreted,
                    [(event_raw, m[0])]
                )

        # 5. Population Queries
        if "population" in normalized_str or "how many people" in normalized_str:
            pop_match = re.search(r"(?:population|people|inhabitants)\s+(?:of|in)?\s*([a-zA-Z\s]+)", normalized_str)
            if pop_match:
                ent_raw = pop_match.group(1).strip()
                m = self.fuzzy_match_entity(ent_raw)
                if m and m[1] in ("country", "city"):
                    interpreted = f"population of {m[0]}"
                    return (
                        Intent.POPULATION_QUERY,
                        Domain.GEOGRAPHY,
                        interpreted,
                        [(ent_raw, m[0])]
                    )

        # 6. Border Queries
        if "border" in normalized_str or "neighbor" in normalized_str:
            border_match = re.search(r"(?:borders?|neighbors?|neighboring)\s+(?:of)?\s*([a-zA-Z\s]+)", normalized_str)
            if border_match:
                ent_raw = border_match.group(1).strip()
                m = self.fuzzy_match_entity(ent_raw)
                if m and m[1] == "country":
                    interpreted = f"bordering countries of {m[0]}"
                    return (
                        Intent.BORDERING_COUNTRIES,
                        Domain.GEOGRAPHY,
                        interpreted,
                        [(ent_raw, m[0])]
                    )

        # 7. Currency Queries
        if "currency" in normalized_str or "money" in normalized_str:
            curr_match = re.search(r"(?:currency|money)\s+(?:of|in)?\s*([a-zA-Z\s]+)", normalized_str)
            if curr_match:
                ent_raw = curr_match.group(1).strip()
                m = self.fuzzy_match_entity(ent_raw)
                if m and m[1] == "country":
                    interpreted = f"currency of {m[0]}"
                    return (
                        Intent.CURRENCY_LOOKUP,
                        Domain.GEOGRAPHY,
                        interpreted,
                        [(ent_raw, m[0])]
                    )

        # 8. Concept Definitions (Civics / Social Studies)
        def_match = re.search(r"(?:what\s+is|define|meaning\s+of|explain)\s+([a-zA-Z\s]+)", normalized_str)
        if def_match:
            concept_raw = def_match.group(1).strip()
            m = self.fuzzy_match_entity(concept_raw)
            if m and m[1] == "concept":
                interpreted = f"definition of {m[0]}"
                return (
                    Intent.DEFINITION,
                    Domain.SOCIAL_STUDIES,
                    interpreted,
                    [(concept_raw, m[0])]
                )

        # 9. General entity scan across the tokens
        # Try n-grams from length 3 down to 1 to find largest matching entity
        all_words = normalized_str.split()
        for n in range(min(4, len(all_words)), 0, -1):
            for i in range(len(all_words) - n + 1):
                ngram = " ".join(all_words[i:i + n])
                m = self.fuzzy_match_entity(ngram)
                if m:
                    canonical, category, _ = m
                    if category == "city":
                        return (
                            Intent.CITY_INFO,
                            Domain.GEOGRAPHY,
                            f"information about {canonical}",
                            [(ngram, canonical)]
                        )
                    elif category == "country":
                        return (
                            Intent.COUNTRY_INFO,
                            Domain.GEOGRAPHY,
                            f"profile of {canonical}",
                            [(ngram, canonical)]
                        )
                    elif category == "event":
                        return (
                            Intent.HISTORICAL_EVENT,
                            Domain.HISTORY,
                            f"historical overview of {canonical}",
                            [(ngram, canonical)]
                        )
                    elif category == "figure":
                        return (
                            Intent.HISTORICAL_FIGURE,
                            Domain.HISTORY,
                            f"biography of {canonical}",
                            [(ngram, canonical)]
                        )
                    elif category == "concept":
                        return (
                            Intent.DEFINITION,
                            Domain.SOCIAL_STUDIES,
                            f"definition of {canonical}",
                            [(ngram, canonical)]
                        )
                    elif category in ("mountain", "river", "ocean", "desert", "island", "lake", "landmark", "strait"):
                        return (
                            Intent.COUNTRY_INFO,
                            Domain.GEOGRAPHY,
                            f"geographic information about {canonical}",
                            [(ngram, canonical)]
                        )
                    elif category == "era":
                        return (
                            Intent.HISTORICAL_EVENT,
                            Domain.HISTORY,
                            f"historical overview of {canonical}",
                            [(ngram, canonical)]
                        )
                    elif category == "organization":
                        return (
                            Intent.DEFINITION,
                            Domain.SOCIAL_STUDIES,
                            f"overview of {canonical}",
                            [(ngram, canonical)]
                        )

        # Default fallback
        return (
            Intent.GENERAL_QA,
            Domain.GENERAL,
            text.strip(),
            []
        )
