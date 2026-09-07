"""
Comparison Engine: Generates structured, side-by-side comparative analysis across Geography, History, and Social Studies.
"""
from typing import Any, Dict, List, Optional
from geomind.core.types import Domain, Intent, QueryResult
from geomind.knowledge.base import KnowledgeSource
from geomind.knowledge.geography import COUNTRIES_DATA, WORLD_CITIES
from geomind.knowledge.history import HISTORICAL_EVENTS, HISTORICAL_FIGURES
from geomind.knowledge.social_studies import SOCIAL_STUDIES_CONCEPTS


class ComparisonEngine(KnowledgeSource):
    """Engine that generates side-by-side comparative studies."""

    @property
    def domain(self) -> Domain:
        return Domain.COMPARISON

    def can_handle(self, intent: Intent, text: str) -> bool:
        return intent == Intent.COMPARISON

    def query(self, intent: Intent, entities: List[str], raw_text: str, context: Optional[str] = None) -> Optional[QueryResult]:
        if len(entities) < 2:
            return None

        ent_a_raw, ent_b_raw = entities[0].lower().strip(), entities[1].lower().strip()

        # 1. Compare Countries
        if ent_a_raw in COUNTRIES_DATA and ent_b_raw in COUNTRIES_DATA:
            ca = COUNTRIES_DATA[ent_a_raw]
            cb = COUNTRIES_DATA[ent_b_raw]

            text = (
                f"⚖️ **Comparative Geography: {ca['name']} vs. {cb['name']}**\n\n"
                f"| Dimension | {ca['name']} | {cb['name']} |\n"
                f"| :--- | :--- | :--- |\n"
                f"| **Official Name** | {ca['official_name']} | {cb['official_name']} |\n"
                f"| **Capital City** | {ca['capital']} | {cb['capital']} |\n"
                f"| **Continent / Region** | {ca['continent']} ({ca['region']}) | {cb['continent']} ({cb['region']}) |\n"
                f"| **Population** | {ca['population']:,} | {cb['population']:,} |\n"
                f"| **Land Area** | {ca['area_sq_km']:,} km² | {cb['area_sq_km']:,} km² |\n"
                f"| **Population Density** | ~{ca['population']/ca['area_sq_km']:.1f} people/km² | ~{cb['population']/cb['area_sq_km']:.1f} people/km² |\n"
                f"| **Currency** | {ca['currency']} | {cb['currency']} |\n"
                f"| **Official Languages** | {', '.join(ca['languages'][:2])} | {', '.join(cb['languages'][:2])} |\n"
                f"| **Land Borders Count** | {len(ca['borders'])} bordering nations | {len(cb['borders'])} bordering nations |\n\n"
                f"### 🌐 Key Takeaways & Differences\n"
                f"- **Demographics**: {ca['name']} has {ca['population']:,} inhabitants compared to {cb['population']:,} in {cb['name']}.\n"
                f"- **Geography & Landmass**: {'larger' if ca['area_sq_km'] > cb['area_sq_km'] else 'smaller'} total land area in {ca['name']} relative to {cb['name']}.\n"
                f"- **Topography**: {ca['name']} features {', '.join(ca['major_features'][:2])}, while {cb['name']} is renowned for {', '.join(cb['major_features'][:2])}."
            )
            return QueryResult(
                text=text,
                interpreted_query=f"comparison between {ca['name']} and {cb['name']}",
                domain=Domain.COMPARISON,
                intent=Intent.COMPARISON,
                entities=[(ent_a_raw, ca['name']), (ent_b_raw, cb['name'])],
                metadata={"type": "countries", "item_a": ca['name'], "item_b": cb['name']},
                sources=["GeoMind Comparative Geographic Dataset"]
            )

        # 2. Compare Cities
        if ent_a_raw in WORLD_CITIES and ent_b_raw in WORLD_CITIES:
            city_a = WORLD_CITIES[ent_a_raw]
            city_b = WORLD_CITIES[ent_b_raw]

            text = (
                f"⚖️ **Comparative Urban Geography: {city_a['name']} vs. {city_b['name']}**\n\n"
                f"| Dimension | {city_a['name']} | {city_b['name']} |\n"
                f"| :--- | :--- | :--- |\n"
                f"| **Country** | {city_a['country']} | {city_b['country']} |\n"
                f"| **Status** | {'Capital City' if city_a['is_capital'] else 'Metropolitan Hub'} | {'Capital City' if city_b['is_capital'] else 'Metropolitan Hub'} |\n"
                f"| **Coordinates** | {city_a['coords']} | {city_b['coords']} |\n"
                f"| **Population** | ~{city_a['population']:,} | ~{city_b['population']:,} |\n\n"
                f"### 🌆 Urban Profiles\n"
                f"- **{city_a['name']}**: {city_a['description']}\n"
                f"- **{city_b['name']}**: {city_b['description']}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"comparison between {city_a['name']} and {city_b['name']}",
                domain=Domain.COMPARISON,
                intent=Intent.COMPARISON,
                entities=[(ent_a_raw, city_a['name']), (ent_b_raw, city_b['name'])],
                metadata={"type": "cities", "item_a": city_a['name'], "item_b": city_b['name']},
                sources=["GeoMind Comparative Urban Dataset"]
            )

        # 3. Compare Historical Events (e.g. WW1 vs WW2)
        event_a = None
        event_b = None
        for k, ev in HISTORICAL_EVENTS.items():
            if ent_a_raw == k or ent_a_raw in ev["aliases"]:
                event_a = ev
            if ent_b_raw == k or ent_b_raw in ev["aliases"]:
                event_b = ev

        if event_a and event_b:
            text = (
                f"⚖️ **Comparative History: {event_a['title']} vs. {event_b['title']}**\n\n"
                f"| Dimension | {event_a['title']} | {event_b['title']} |\n"
                f"| :--- | :--- | :--- |\n"
                f"| **Period** | {event_a['period']} | {event_b['period']} |\n"
                f"| **Primary Nature** | Great Power trench warfare / imperial clash | Total global warfare, mechanized blitzkrieg, ideological conflict |\n"
                f"| **Key Trigger / Catalyst** | Sarajevo assassination of Franz Ferdinand | Nazi invasion of Poland (1939) |\n"
                f"| **Major Outcomes** | Treaty of Versailles, League of Nations, fall of 4 empires | Creation of UN, Atomic Age, Cold War, Decolonization |\n\n"
                f"### 🔍 Historical Continuity\n"
                f"Many historians analyze {event_b['title']} as intimately linked to the unresolved geopolitical, territorial, and economic grievances created in the aftermath of {event_a['title']}."
            )
            return QueryResult(
                text=text,
                interpreted_query=f"comparison between {event_a['title']} and {event_b['title']}",
                domain=Domain.COMPARISON,
                intent=Intent.COMPARISON,
                entities=[(ent_a_raw, event_a['title']), (ent_b_raw, event_b['title'])],
                metadata={"type": "historical_events", "item_a": event_a['title'], "item_b": event_b['title']},
                sources=["GeoMind Comparative History Dataset"]
            )

        # 4. Compare Social Studies Concepts (e.g. Capitalism vs Socialism, Democracy vs Republic)
        con_a = SOCIAL_STUDIES_CONCEPTS.get(ent_a_raw)
        con_b = SOCIAL_STUDIES_CONCEPTS.get(ent_b_raw)
        if con_a and con_b:
            text = (
                f"⚖️ **Comparative Social Studies: {con_a['term']} vs. {con_b['term']}**\n\n"
                f"| Dimension | {con_a['term']} | {con_b['term']} |\n"
                f"| :--- | :--- | :--- |\n"
                f"| **Category** | {con_a['category']} | {con_b['category']} |\n"
                f"| **Core Concept** | {con_a['definition']} | {con_b['definition']} |\n\n"
                f"### ⚙️ Core Philosophical Distinction\n"
                f"- **{con_a['term']}**: Emphasizes {con_a['key_characteristics'][0]}.\n"
                f"- **{con_b['term']}**: Emphasizes {con_b['key_characteristics'][0]}.\n\n"
                f"### 🌐 Real-World Applications\n"
                f"- **{con_a['term']} Examples**: {', '.join(con_a['examples'])}\n"
                f"- **{con_b['term']} Examples**: {', '.join(con_b['examples'])}"
            )
            return QueryResult(
                text=text,
                interpreted_query=f"comparison between {con_a['term']} and {con_b['term']}",
                domain=Domain.COMPARISON,
                intent=Intent.COMPARISON,
                entities=[(ent_a_raw, con_a['term']), (ent_b_raw, con_b['term'])],
                metadata={"type": "social_studies", "item_a": con_a['term'], "item_b": con_b['term']},
                sources=["GeoMind Social Studies Comparative Matrix"]
            )

        return None
