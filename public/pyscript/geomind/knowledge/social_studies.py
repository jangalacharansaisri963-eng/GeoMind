"""
Comprehensive Social Studies Knowledge Base: Civics, Government Systems, Economics, Sociology, and Human Geography.
"""
from typing import Any, Dict, List, Optional
import os
import json
from geomind.core.types import Domain, Intent, QueryResult
from geomind.knowledge.base import KnowledgeSource


_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load_ss_json(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(_DATA_DIR, filename)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


SOCIAL_STUDIES_CONCEPTS: Dict[str, Dict[str, Any]] = {
    "democracy": {
        "term": "Democracy",
        "category": "Civics & Government",
        "aliases": ["democratic government", "direct democracy", "representative democracy"],
        "definition": "A system of government in which political power is vested in the people, who rule either directly or through freely elected representatives.",
        "key_characteristics": [
            "Free, fair, periodic, and competitive multi-party elections.",
            "Universal suffrage and active political participation by citizens.",
            "Protection of fundamental civil liberties, minority rights, and freedom of speech/press.",
            "Adherence to the Rule of Law and constitutional constraints on authority."
        ],
        "historical_context": "Originated in ancient Athens around the 5th century BC (direct democracy), and evolved during the Enlightenment and modern revolutions into constitutional representative democracy.",
        "examples": ["United States", "India", "United Kingdom", "France", "Japan"]
    },
    "republic": {
        "term": "Republic",
        "category": "Civics & Government",
        "aliases": ["constitutional republic", "republicanism"],
        "definition": "A form of government in which the country is considered a 'public matter' (res publica), where the head of state is elected or appointed, not a hereditary monarch, and power is constrained by a constitution.",
        "key_characteristics": [
            "Absence of hereditary monarchy.",
            "Government officials are representatives of the citizen body and govern according to established constitutional law.",
            "Protection of individual and minority rights against potential tyranny of the majority."
        ],
        "historical_context": "The Roman Republic (c. 509 BC – 27 BC) established fundamental checks, balances, and senatorial representation that shaped modern constitutional republics.",
        "examples": ["United States", "France", "Germany", "India", "Brazil"]
    },
    "federalism": {
        "term": "Federalism",
        "category": "Civics & Government",
        "aliases": ["federal system", "federation"],
        "definition": "A constitutional division of political power between a central national government and regional or state governing authorities.",
        "key_characteristics": [
            "Dual sovereignty: both central and state governments hold distinct constitutional powers.",
            "Written constitution that cannot be unilaterally altered by one level of government alone.",
            "Independent judiciary to arbitrate disputes between federal and state authorities."
        ],
        "historical_context": "Prominently codified in the 1787 United States Constitution to balance strong central unity with local state autonomy, later adopted by diverse nations like India, Canada, Germany, and Australia.",
        "examples": ["United States (50 states)", "India (28 states)", "Germany (16 Länder)", "Canada (10 provinces)"]
    },
    "separation of powers": {
        "term": "Separation of Powers",
        "category": "Civics & Government",
        "aliases": ["checks and balances", "trias politica"],
        "definition": "A constitutional doctrine dividing governmental responsibilities into distinct branches—Legislative, Executive, and Judicial—to prevent any single group or individual from accumulating tyrannical power.",
        "key_characteristics": [
            "Legislative: Drafts and enacts laws (e.g., Congress or Parliament).",
            "Executive: Administers, enforces, and implements laws (e.g., President or Prime Minister).",
            "Judicial: Interprets laws and adjudicates disputes (e.g., Supreme Court).",
            "Checks and Balances: Each branch possesses specific powers to limit and monitor the others."
        ],
        "historical_context": "Formulated by French Enlightenment philosopher Montesquieu in 'The Spirit of the Laws' (1748), heavily influencing the U.S. Constitution and modern democratic frameworks.",
        "examples": ["United States Federal Government", "South Korea", "Brazil", "France"]
    },
    "capitalism": {
        "term": "Capitalism",
        "category": "Economics",
        "aliases": ["free market", "market economy"],
        "definition": "An economic system characterized by private ownership of the means of production, competitive markets, voluntary exchange, and capital accumulation motivated by profit.",
        "key_characteristics": [
            "Private property rights and freedom of enterprise.",
            "Price mechanisms determined predominantly by supply and demand rather than central planning.",
            "Incentive for technological innovation, efficiency, and capital investment.",
            "Role of government primarily focused on enforcing contracts, maintaining rule of law, and regulating market failures."
        ],
        "historical_context": "Articulated by Scottish philosopher Adam Smith in 'The Wealth of Nations' (1776), describing the 'invisible hand' of market coordination during the Industrial Revolution.",
        "examples": ["United States", "Singapore", "Switzerland", "United Kingdom"]
    },
    "socialism": {
        "term": "Socialism",
        "category": "Economics & Political Theory",
        "aliases": ["democratic socialism", "planned economy"],
        "definition": "An economic and political system emphasizing social or collective ownership and democratic administration of the means of production and distribution, aimed at achieving socio-economic equality.",
        "key_characteristics": [
            "Public, state, or cooperative control over major industries and public utilities.",
            "Redistribution of wealth through progressive taxation, universal healthcare, and public welfare.",
            "Production directed toward satisfying human social needs rather than purely generating private profit."
        ],
        "historical_context": "Emerged as a critique of the harsh inequalities and labor exploitation of 19th-century industrial capitalism, developed by Robert Owen, Karl Marx, and later democratic socialist traditions in Europe.",
        "examples": ["Nordic model social democracies (Sweden, Norway, Denmark combining market economies with strong socialist welfare safety nets)"]
    },
    "urbanization": {
        "term": "Urbanization",
        "category": "Human Geography & Sociology",
        "aliases": ["urban sprawl", "city growth"],
        "definition": "The progressive demographic and spatial process by which rural populations migrate to and concentrate in urban cities and metropolitan areas.",
        "key_characteristics": [
            "Driven by 'push factors' (rural poverty, crop failures) and 'pull factors' (urban industrial jobs, education, superior infrastructure).",
            "Rise of megacities (urban metropolitan areas with over 10 million residents).",
            "Associated environmental challenges: traffic congestion, housing shortages, heat island effect, and public sanitation needs."
        ],
        "historical_context": "Accelerated exponentially during the Industrial Revolution as factory mechanization centralized labor, continuing today rapidly across the Global South.",
        "examples": ["Tokyo", "Delhi", "Shanghai", "São Paulo", "Lagos"]
    },
    "mercantilism": {
        "term": "Mercantilism",
        "category": "Economic History",
        "aliases": ["mercantilist system"],
        "definition": "An economic policy dominant in Europe from the 16th to 18th centuries, designed to maximize a nation's wealth and power through a favorable balance of trade, accumulating gold and silver bullion, and exploiting colonial resources.",
        "key_characteristics": [
            "Colonies served as captive markets and exclusive sources of cheap raw materials for the mother country.",
            "High tariffs on foreign manufactured imports to protect domestic industries.",
            "State monopolies and government subsidies granted to domestic chartered trading corporations (e.g., British and Dutch East India Companies)."
        ],
        "historical_context": "Fuelled colonial expansion and imperial rivalries across the Atlantic and Indian Oceans until superseded by classical free-market economics in the late 18th century.",
        "examples": ["17th-century British Empire Navigation Acts", "Colbertism in France"]
    }
}

# Ingest expanded Wikipedia datasets into SOCIAL_STUDIES_CONCEPTS
for _gov in _load_ss_json("forms_of_government.json"):
    _k = _gov.get("name", "").lower()
    if _k and _k not in SOCIAL_STUDIES_CONCEPTS:
        SOCIAL_STUDIES_CONCEPTS[_k] = {
            "term": _gov.get("name", ""),
            "category": "Forms of Government",
            "aliases": [_gov.get("etymology", "")] if _gov.get("etymology") else [],
            "definition": _gov.get("definition", _gov.get("description", "")),
            "key_characteristics": _gov.get("core_principles", _gov.get("subtypes", [])),
            "historical_context": _gov.get("description", ""),
            "examples": _gov.get("subtypes", [])
        }

for _ec in _load_ss_json("economic_systems.json"):
    _k = _ec.get("name", "").lower()
    if _k and _k not in SOCIAL_STUDIES_CONCEPTS:
        SOCIAL_STUDIES_CONCEPTS[_k] = {
            "term": _ec.get("name", ""),
            "category": "Economic Systems",
            "aliases": [],
            "definition": _ec.get("definition", _ec.get("description", "")),
            "key_characteristics": _ec.get("core_tenets", []),
            "historical_context": f"Key Thinkers: {', '.join(_ec.get('key_thinkers', []))}. {_ec.get('description', '')}",
            "examples": _ec.get("advantages", [])
        }

for _org in _load_ss_json("international_organizations.json"):
    _k = _org.get("name", "").lower()
    if _k and _k not in SOCIAL_STUDIES_CONCEPTS:
        SOCIAL_STUDIES_CONCEPTS[_k] = {
            "term": _org.get("name", ""),
            "category": "International Organizations",
            "aliases": [_org.get("id", "").lower()],
            "definition": _org.get("mission", _org.get("description", "")),
            "key_characteristics": [
                f"Founded: {_org.get('founded', 'N/A')}",
                f"Headquarters: {_org.get('headquarters', 'N/A')}",
                f"Member States: {_org.get('member_states', 'N/A')}"
            ],
            "historical_context": _org.get("description", ""),
            "examples": _org.get("principal_organs", [])
        }

for _cp in _load_ss_json("constitutional_principles.json"):
    _k = _cp.get("name", "").lower()
    if _k and _k not in SOCIAL_STUDIES_CONCEPTS:
        SOCIAL_STUDIES_CONCEPTS[_k] = {
            "term": _cp.get("name", ""),
            "category": "Constitutional Law & Governance",
            "aliases": [],
            "definition": _cp.get("definition", ""),
            "key_characteristics": _cp.get("mechanisms", []),
            "historical_context": f"Prominent Theorist: {_cp.get('theorist', 'N/A')}. Purpose: {_cp.get('purpose', '')}",
            "examples": _cp.get("mechanisms", [])
        }


class SocialStudiesKnowledgeSource(KnowledgeSource):
    """Knowledge source for civics, economics, government systems, and sociology."""

    @property
    def domain(self) -> Domain:
        return Domain.SOCIAL_STUDIES

    def can_handle(self, intent: Intent, text: str) -> bool:
        return intent == Intent.DEFINITION or any(
            concept in text.lower() for concept in SOCIAL_STUDIES_CONCEPTS
        )

    def find_concept(self, query: str) -> Optional[Dict[str, Any]]:
        clean = query.strip().lower()
        if clean in SOCIAL_STUDIES_CONCEPTS:
            return SOCIAL_STUDIES_CONCEPTS[clean]
        for key, concept in SOCIAL_STUDIES_CONCEPTS.items():
            if clean in concept["aliases"] or clean in key or any(alias in clean for alias in concept["aliases"]):
                return concept
        return None

    def query(self, intent: Intent, entities: List[str], raw_text: str, context: Optional[str] = None) -> Optional[QueryResult]:
        concept_data = None
        target_term = ""

        # Try entities first
        if entities:
            concept_data = self.find_concept(entities[0])
            target_term = entities[0]

        # If not found via entities, scan raw text
        if not concept_data:
            for key in SOCIAL_STUDIES_CONCEPTS:
                if key in raw_text.lower():
                    concept_data = SOCIAL_STUDIES_CONCEPTS[key]
                    target_term = key
                    break

        if not concept_data:
            return None

        characteristics = "\n".join(f"- {c}" for c in concept_data["key_characteristics"])
        examples_str = ", ".join(concept_data["examples"])

        text = (
            f"📚 **Social Studies Concept: {concept_data['term']}**\n\n"
            f"**Field**: {concept_data['category']}\n\n"
            f"### 💡 Core Definition\n"
            f"{concept_data['definition']}\n\n"
            f"### ⚙️ Fundamental Characteristics\n"
            f"{characteristics}\n\n"
            f"### 🏛️ Historical Context & Evolution\n"
            f"{concept_data['historical_context']}\n\n"
            f"### 🌐 Contemporary & Historical Examples\n"
            f"{examples_str}"
        )

        return QueryResult(
            text=text,
            interpreted_query=f"definition and concept of {concept_data['term']}",
            domain=Domain.SOCIAL_STUDIES,
            intent=Intent.DEFINITION,
            entities=[(target_term, concept_data["term"])],
            metadata=concept_data,
            sources=["GeoMind Civics & Social Sciences Encyclopedia"]
        )
