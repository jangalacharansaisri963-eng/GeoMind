"""
Built-in offline knowledge reasoning engine for GeoMind.
"""
import random
from typing import Any, Dict, List, Optional
from geomind.core.types import Domain, Intent, QueryResult, GeoCoord
from geomind.core.nlp import NLPEngine
from geomind.knowledge.distance import compute_distance
from geomind.knowledge.geography import GeographyKnowledgeSource
from geomind.knowledge.history import HistoryKnowledgeSource
from geomind.knowledge.social_studies import SocialStudiesKnowledgeSource
from geomind.knowledge.comparison import ComparisonEngine
from geomind.knowledge.web_research import WebResearchEngine
from geomind.knowledge.rag import RagEngine, get_rag_engine
from geomind.models.base import ModelProvider


GREETING_RESPONSES = [
    "Hey there! 👋 I'm GeoMind — ask me anything about geography, history, or social studies.",
    "Hi! 🌍 Ready when you are — try a country, a historical event, or a civics question.",
    "Hello! Good to see you. What geography, history, or social studies question is on your mind?",
    "Yo! 😄 GeoMind here. Ask about distances, capitals, wars, revolutions, or governments — I've got you.",
    "Hey! What's up — want to explore a country profile, a historical event, or a social studies concept?",
]

TIME_OF_DAY_RESPONSES = {
    "morning": "Good morning! ☀️ Ready to explore some geography or history today?",
    "afternoon": "Good afternoon! 🌤️ What would you like to learn about?",
    "evening": "Good evening! 🌆 Ask me about a place, an era, or a civics concept.",
}


class RuleEngine(ModelProvider):
    """Core offline semantic and knowledge-graph reasoner."""

    def __init__(self):
        self.nlp = NLPEngine()
        self.geo_source = GeographyKnowledgeSource()
        self.history_source = HistoryKnowledgeSource()
        self.social_source = SocialStudiesKnowledgeSource()
        self.compare_source = ComparisonEngine()
        self.web_research = WebResearchEngine()
        self.rag = get_rag_engine()

    @property
    def name(self) -> str:
        return "geomind-symbolic-reasoner"

    def generate(
        self,
        query: str,
        context: Optional[List[Dict[str, Any]]] = None,
        system_instruction: Optional[str] = None
    ) -> QueryResult:
        # Handle contextual follow-ups (e.g. "what were its causes", "tell me about its capital")
        effective_query = query
        if context and len(context) > 0:
            last_msg = context[-1]
            last_metadata = last_msg.get("metadata", {})
            last_subject = None
            if "name" in last_metadata:
                last_subject = last_metadata["name"]
            elif "country" in last_metadata:
                last_subject = last_metadata["country"]
            elif "title" in last_metadata:
                last_subject = last_metadata["title"]
            elif "term" in last_metadata:
                last_subject = last_metadata["term"]

            if last_subject and any(pronoun in query.lower().split() for pronoun in ("it", "its", "they", "their", "there")):
                effective_query = f"{query} of {last_subject}"

        # 1. NLP parsing and fuzzy normalization
        intent, domain, interpreted_query, entities = self.nlp.extract_entities_and_intent(effective_query)
        resolved_entities_list = [canonical for _, canonical in entities]

        # 1b. Casual greetings ("hi", "hello", "good morning", "what's up", etc.)
        if intent == Intent.GREETING:
            lower_q = query.lower()
            if "morning" in lower_q:
                text = TIME_OF_DAY_RESPONSES["morning"]
            elif "afternoon" in lower_q:
                text = TIME_OF_DAY_RESPONSES["afternoon"]
            elif "evening" in lower_q:
                text = TIME_OF_DAY_RESPONSES["evening"]
            else:
                text = random.choice(GREETING_RESPONSES)
            return QueryResult(
                text=text,
                interpreted_query=interpreted_query,
                domain=Domain.GENERAL,
                intent=Intent.GREETING,
                entities=entities,
                sources=["GeoMind Conversational Layer"]
            )

        # 2. Distance queries
        if intent == Intent.DISTANCE_CALCULATION and len(resolved_entities_list) >= 2:
            loc1_name = resolved_entities_list[0]
            loc2_name = resolved_entities_list[1]

            res1 = self.geo_source.resolve_location(loc1_name)
            res2 = self.geo_source.resolve_location(loc2_name)

            if res1 and res2:
                std_name1, coords1, data1 = res1
                std_name2, coords2, data2 = res2
                dist_res = compute_distance(std_name1, coords1, std_name2, coords2)

                drive_line = f"- **Driving Time Estimate**: ~{dist_res.driving_time_hours:.1f} hours (land route approximation)" if dist_res.driving_time_hours else ""
                
                text = (
                    f"📏 **Geodesic Distance: {std_name1} ➔ {std_name2}**\n\n"
                    f"{dist_res.context}\n\n"
                    f"### 📍 Geographic & Routing Details\n"
                    f"- **Direct Great-Circle Distance**: **{dist_res.distance_km:,.1f} km** ({dist_res.distance_miles:,.1f} miles)\n"
                    f"- **Compass Bearing**: **{dist_res.bearing_degrees:.1f}°** ({dist_res.compass_direction})\n"
                    f"- **Origin Coordinates**: {coords1} ({std_name1})\n"
                    f"- **Destination Coordinates**: {coords2} ({std_name2})\n"
                    f"- **Commercial Flight Duration**: ~{dist_res.flight_time_hours:.1f} hours\n"
                    f"{drive_line}".strip()
                )

                return QueryResult(
                    text=text,
                    interpreted_query=interpreted_query,
                    domain=Domain.DISTANCE,
                    intent=Intent.DISTANCE_CALCULATION,
                    entities=entities,
                    metadata={
                        "origin": std_name1,
                        "destination": std_name2,
                        "distance_km": dist_res.distance_km,
                        "distance_miles": dist_res.distance_miles,
                        "bearing": dist_res.bearing_degrees,
                        "compass_direction": dist_res.compass_direction,
                        "origin_coords": (coords1.lat, coords1.lon),
                        "dest_coords": (coords2.lat, coords2.lon)
                    },
                    sources=["GeoMind Geodesic Calculator (Haversine WGS84)"]
                )

        # 3. Comparison queries
        if intent == Intent.COMPARISON and len(resolved_entities_list) >= 2:
            res = self.compare_source.query(intent, resolved_entities_list, query)
            if res:
                res.interpreted_query = interpreted_query
                return res

        # 4. Geography queries
        if domain == Domain.GEOGRAPHY:
            res = self.geo_source.query(intent, resolved_entities_list, query)
            if res:
                res.interpreted_query = interpreted_query
                return res

        # 5. History queries
        if domain == Domain.HISTORY:
            res = self.history_source.query(intent, resolved_entities_list, query)
            if res:
                res.interpreted_query = interpreted_query
                return res

        # 6. Social Studies queries
        if domain == Domain.SOCIAL_STUDIES:
            res = self.social_source.query(intent, resolved_entities_list, query)
            if res:
                res.interpreted_query = interpreted_query
                return res

        # 7. Fallback / General QA
        # Check if query matches any entity in any source
        if resolved_entities_list:
            res_geo = self.geo_source.query(intent, resolved_entities_list, query)
            if res_geo:
                return res_geo
            res_hist = self.history_source.query(intent, resolved_entities_list, query)
            if res_hist:
                return res_hist
            res_soc = self.social_source.query(intent, resolved_entities_list, query)
            if res_soc:
                return res_soc

        # 7b. Offline RAG fallback — retrieve from local knowledge corpus
        # before going to the network.
        if self.rag.is_available() and len(query.split()) > 2:
            rag_result = self.rag.query(query)
            if rag_result:
                rag_result.interpreted_query = interpreted_query
                rag_result.entities = entities
                # Keep the original intent if it was meaningful, otherwise mark as RAG
                if rag_result.intent == Intent.GENERAL_QA:
                    rag_result.intent = Intent.RAG
                return rag_result

        # 7c. Live web research fallback (Google / Playwright), only for
        # substantive questions that still didn't match anything.
        if self.web_research.is_available() and len(query.split()) > 2:
            web_result = self.web_research.research(query)
            if web_result:
                return QueryResult(
                    text=web_result.text,
                    interpreted_query=interpreted_query,
                    domain=Domain.GENERAL,
                    intent=Intent.WEB_RESEARCH,
                    entities=entities,
                    metadata={"web_query": query},
                    sources=web_result.sources
                )

        # Helpful explanatory answer for general social studies / geo / history
        response_text = (
            f"🌐 **GeoMind Social Studies Knowledge Base**\n\n"
            f"I analyzed your query: *\"{query}\"*\n\n"
            f"GeoMind specializes in:\n"
            f"- **Geography**: Country profiles, capitals, borders, currencies, coordinates, populations.\n"
            f"- **Distance Calculation**: Exact geodesic distances, bearings, and travel estimates (e.g., *'distance between Delhi and Mumbai'*).\n"
            f"- **History**: Major historical events, eras, causes and consequences (e.g., *'causes of World War 1'*, *'French Revolution'*).\n"
            f"- **Historical Figures**: Biographies, achievements, and impact (e.g., *'Napoleon Bonaparte'*, *'Mahatma Gandhi'*).\n"
            f"- **Social Studies**: Civics, governance systems, economic models, sociology (e.g., *'what is federalism'*, *'capitalism'*).\n"
            f"- **Comparative Analysis**: Side-by-side breakdowns (e.g., *'compare India and China'*, *'capitalism vs socialism'*).\n\n"
            f"💡 *Tip: Try asking about a specific nation, city, historical event, or concept.*"
        )
        return QueryResult(
            text=response_text,
            interpreted_query=interpreted_query,
            domain=Domain.GENERAL,
            intent=Intent.GENERAL_QA,
            entities=entities,
            sources=["GeoMind Knowledge System"]
        )
