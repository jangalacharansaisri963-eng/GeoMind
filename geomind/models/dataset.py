"""
GeoMind Dataset: High-quality supervised and reasoning datasets for Geography, History, and Social Studies.
Includes curated training pairs, synthetic data augmentation, and dataset loaders.
"""
import json
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from geomind.core.types import Domain, Intent


@dataclass
class TrainingExample:
    prompt: str
    response: str
    domain_id: int
    intent_id: int
    entities: List[str]


# Domain mapping:
# 0: GENERAL, 1: GEOGRAPHY, 2: HISTORY, 3: SOCIAL_STUDIES, 4: DISTANCE, 5: COMPARISON
DOMAIN_TO_ID = {
    Domain.GENERAL: 0,
    Domain.GEOGRAPHY: 1,
    Domain.HISTORY: 2,
    Domain.SOCIAL_STUDIES: 3,
    Domain.DISTANCE: 4,
    Domain.COMPARISON: 5
}

ID_TO_DOMAIN = {v: k for k, v in DOMAIN_TO_ID.items()}

# Intent mapping:
INTENT_TO_ID = {
    Intent.GENERAL_QA: 0,
    Intent.CAPITAL_LOOKUP: 1,
    Intent.DISTANCE_CALCULATION: 2,
    Intent.COUNTRY_INFO: 3,
    Intent.HISTORICAL_EVENT: 4,
    Intent.HISTORICAL_FIGURE: 5,
    Intent.CAUSE_AND_CONSEQUENCE: 6,
    Intent.DEFINITION: 7,
    Intent.COMPARISON: 8,
    Intent.POPULATION_QUERY: 9
}

ID_TO_INTENT = {v: k for k, v in INTENT_TO_ID.items()}


BASE_TRAINING_EXAMPLES = [
    # 1. Geography & Capitals
    TrainingExample(
        prompt="what is the capital of France",
        response="The capital of France is Paris. Paris is situated along the Seine River in north-central France.",
        domain_id=1, intent_id=1, entities=["France", "Paris"]
    ),
    TrainingExample(
        prompt="capital of Japan",
        response="The capital of Japan is Tokyo, the most populous metropolitan area on Earth.",
        domain_id=1, intent_id=1, entities=["Japan", "Tokyo"]
    ),
    TrainingExample(
        prompt="what is the capital of India",
        response="The capital of India is New Delhi, located in the National Capital Territory of Delhi in northern India.",
        domain_id=1, intent_id=1, entities=["India", "New Delhi"]
    ),
    TrainingExample(
        prompt="tell me about Germany",
        response="Germany is a federal parliamentary republic in Central Europe. Its capital is Berlin, currency is Euro, and it shares land borders with nine nations.",
        domain_id=1, intent_id=3, entities=["Germany", "Berlin"]
    ),
    TrainingExample(
        prompt="what is the population of Tokyo",
        response="Tokyo metropolis has an urban population of approximately 14 million, with greater metropolitan area exceeding 37 million residents.",
        domain_id=1, intent_id=9, entities=["Tokyo"]
    ),

    # 2. Distance Calculations (including typos & informal phrasing)
    TrainingExample(
        prompt="ditace between delhi & mumbi",
        response="The great-circle geodesic distance between Delhi and Mumbai is approximately 1,148.1 km (713.4 miles) with a bearing of 203.5° south-southwest.",
        domain_id=4, intent_id=2, entities=["Delhi", "Mumbai"]
    ),
    TrainingExample(
        prompt="how far is London from Paris",
        response="The direct great-circle distance from London to Paris is 343.8 km (213.6 miles) across the English Channel.",
        domain_id=4, intent_id=2, entities=["London", "Paris"]
    ),
    TrainingExample(
        prompt="distance between Tokyo and Sydney",
        response="The great-circle distance between Tokyo, Japan and Sydney, Australia is approximately 7,825 km (4,862 miles).",
        domain_id=4, intent_id=2, entities=["Tokyo", "Sydney"]
    ),

    # 3. History: Causes, Consequences, and Figures
    TrainingExample(
        prompt="causes and consequences of World War 1",
        response="World War I (1914–1918) was caused by Militarism, Alliances, Imperialism, and Nationalism (M-A-I-N), catalyzed by the assassination of Archduke Franz Ferdinand. Consequences included the collapse of four empires, Treaty of Versailles, and League of Nations creation.",
        domain_id=2, intent_id=6, entities=["World War I"]
    ),
    TrainingExample(
        prompt="causes of the French Revolution",
        response="Key causes included deep financial insolvency from foreign wars, the unjust Three Estates social hierarchy, Enlightenment political philosophy, and severe agricultural crop failures in 1788–1789.",
        domain_id=2, intent_id=6, entities=["French Revolution"]
    ),
    TrainingExample(
        prompt="who was Napoleon Bonaparte",
        response="Napoleon Bonaparte (1769–1821) was a French military commander and statesman who seized power in 1799, codified civil law in the Napoleonic Code, and conquered much of continental Europe.",
        domain_id=2, intent_id=5, entities=["Napoleon Bonaparte"]
    ),
    TrainingExample(
        prompt="who was Mahatma Gandhi",
        response="Mahatma Gandhi (1869–1948) was an Indian lawyer and anti-colonial leader who pioneered Satyagraha (nonviolent civil disobedience), successfully guiding India to independence from British rule in 1947.",
        domain_id=2, intent_id=5, entities=["Mahatma Gandhi"]
    ),

    # 4. Social Studies, Civics, and Economics
    TrainingExample(
        prompt="what is democracy",
        response="Democracy is a system of government in which sovereign power is vested in the people, exercised through free and fair elections, rule of law, and institutional protection of civil liberties.",
        domain_id=3, intent_id=7, entities=["Democracy"]
    ),
    TrainingExample(
        prompt="define federalism",
        response="Federalism is a constitutional mode of political organization uniting separate states or polities within an overarching political system, dividing powers between central and regional governments.",
        domain_id=3, intent_id=7, entities=["Federalism"]
    ),
    TrainingExample(
        prompt="what is capitalism",
        response="Capitalism is an economic system characterized by private ownership of production, voluntary market exchange, price determination by supply and demand, and capital accumulation motivated by profit.",
        domain_id=3, intent_id=7, entities=["Capitalism"]
    ),
    TrainingExample(
        prompt="what is separation of powers",
        response="Separation of powers is the constitutional doctrine dividing state authority into three distinct branches—Legislative, Executive, and Judicial—with mutual checks and balances preventing tyranny.",
        domain_id=3, intent_id=7, entities=["Separation of Powers"]
    ),

    # 5. Comparative Analysis
    TrainingExample(
        prompt="compare capitalism and socialism",
        response="Capitalism relies on private ownership and competitive market pricing; socialism emphasizes collective or public ownership of major means of production to ensure equitable distribution of wealth and resources.",
        domain_id=5, intent_id=8, entities=["Capitalism", "Socialism"]
    ),
    TrainingExample(
        prompt="compare India and China",
        response="India and China are the two most populous countries. India operates as a federal democratic republic with a service-driven market economy, while China operates under a single-party socialist system with state-directed industrial manufacturing.",
        domain_id=5, intent_id=8, entities=["India", "China"]
    )
]


def generate_wikipedia_training_dataset() -> List[TrainingExample]:
    """
    Constructs high-quality supervised training pairs dynamically by parsing
    the 18 structured Wikipedia and geographic/historical JSON datasets in geomind/data/.
    """
    import os
    examples: List[TrainingExample] = []
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    if not os.path.exists(data_dir):
        return examples

    def load_json_file(fname: str) -> List[Dict[str, Any]]:
        fpath = os.path.join(data_dir, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    # 1. Mountains (Geography)
    mountains = load_json_file("mountains.json")
    for m in mountains:
        name = m.get("name", "")
        elev_m = m.get("elevation_m", 0)
        rng = m.get("range", "")
        countries = ", ".join(m.get("countries", []))
        desc = m.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is {name}",
            response=f"{name} is a major mountain peak ({elev_m} m) in the {rng}, located in {countries}. {desc}",
            domain_id=1, intent_id=0, entities=[name]
        ))
        examples.append(TrainingExample(
            prompt=f"elevation of {name}",
            response=f"{name} stands at an elevation of {elev_m} meters ({m.get('elevation_ft', 0)} feet).",
            domain_id=1, intent_id=0, entities=[name]
        ))

    # 2. Rivers (Geography)
    rivers = load_json_file("rivers.json")
    for r in rivers:
        name = r.get("name", "")
        len_km = r.get("length_km", 0)
        outflow = r.get("outflow", "")
        desc = r.get("description", "")
        examples.append(TrainingExample(
            prompt=f"tell me about the {name}",
            response=f"{name} has a length of {len_km:,} km, discharging into the {outflow}. {desc}",
            domain_id=1, intent_id=0, entities=[name]
        ))
        examples.append(TrainingExample(
            prompt=f"where does the {name} flow into",
            response=f"{name} drains into the {outflow}.",
            domain_id=1, intent_id=0, entities=[name]
        ))

    # 3. Oceans & Seas (Geography)
    oceans = load_json_file("oceans_seas.json")
    for o in oceans:
        name = o.get("name", "")
        deepest = o.get("deepest_point", "")
        desc = o.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is the {name}",
            response=f"{name} is one of Earth's major oceanic divisions. Deepest point: {deepest}. {desc}",
            domain_id=1, intent_id=0, entities=[name]
        ))

    # 4. Deserts (Geography)
    deserts = load_json_file("deserts.json")
    for d in deserts:
        name = d.get("name", "")
        area = d.get("area_sq_km", 0)
        dtype = d.get("type", "")
        desc = d.get("description", "")
        examples.append(TrainingExample(
            prompt=f"tell me about the {name}",
            response=f"{name} is a {dtype} desert covering approximately {area:,} km². {desc}",
            domain_id=1, intent_id=0, entities=[name]
        ))

    # 5. Islands (Geography)
    islands = load_json_file("islands.json")
    for i in islands:
        name = i.get("name", "")
        area = i.get("area_sq_km", 0)
        desc = i.get("description", "")
        examples.append(TrainingExample(
            prompt=f"tell me about {name}",
            response=f"{name} covers an area of {area:,} km². {desc}",
            domain_id=1, intent_id=0, entities=[name]
        ))

    # 6. Lakes (Geography)
    lakes = load_json_file("lakes.json")
    for l in lakes:
        name = l.get("name", "")
        depth = l.get("max_depth_m", 0)
        desc = l.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is {name}",
            response=f"{name} is a prominent inland body of water with a maximum depth of {depth} m. {desc}",
            domain_id=1, intent_id=0, entities=[name]
        ))

    # 7. World Wonders & Landmarks (Geography & History)
    wonders = load_json_file("world_wonders_landmarks.json")
    for w in wonders:
        name = w.get("name", "")
        loc = w.get("location", "")
        country = w.get("country", "")
        desc = w.get("description", "")
        examples.append(TrainingExample(
            prompt=f"where is {name}",
            response=f"{name} is located in {loc}, {country}. {desc}",
            domain_id=1, intent_id=0, entities=[name, country]
        ))

    # 8. Geographical Extremes (Geography)
    extremes = load_json_file("geographical_extremes.json")
    for ex in extremes:
        rec = ex.get("record", "")
        feat = ex.get("feature", "")
        val = ex.get("value", "")
        desc = ex.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is the {rec.lower()}",
            response=f"The {rec.lower()} is {feat} ({val}). {desc}",
            domain_id=1, intent_id=0, entities=[feat]
        ))

    # 9. Straits and Canals (Geography)
    straits = load_json_file("straits_and_canals.json")
    for st in straits:
        name = st.get("name", "")
        conn = " and ".join(st.get("connects", []))
        desc = st.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is the {name}",
            response=f"{name} is a vital maritime passage connecting the {conn}. {desc}",
            domain_id=1, intent_id=0, entities=[name]
        ))

    # 10. Historical Eras (History)
    eras = load_json_file("historical_eras.json")
    for er in eras:
        name = er.get("name", "")
        period = er.get("period", "")
        desc = er.get("description", "")
        examples.append(TrainingExample(
            prompt=f"tell me about {name}",
            response=f"{name} spanned {period}. {desc}",
            domain_id=2, intent_id=4, entities=[name]
        ))

    # 11. Historical Events (History)
    events = load_json_file("historical_events.json")
    for ev in events:
        name = ev.get("name", "")
        causes = "; ".join(ev.get("causes", [])[:3])
        conseq = "; ".join(ev.get("consequences", [])[:3])
        desc = ev.get("description", "")
        examples.append(TrainingExample(
            prompt=f"causes of {name}",
            response=f"Key causes of {name} included: {causes}.",
            domain_id=2, intent_id=6, entities=[name]
        ))
        examples.append(TrainingExample(
            prompt=f"consequences of {name}",
            response=f"Primary consequences of {name} included: {conseq}.",
            domain_id=2, intent_id=6, entities=[name]
        ))

    # 12. Historical Figures (History)
    figures = load_json_file("historical_figures.json")
    for fig in figures:
        name = fig.get("name", "")
        title = fig.get("title", "")
        achieve = "; ".join(fig.get("key_achievements", [])[:2])
        desc = fig.get("description", "")
        examples.append(TrainingExample(
            prompt=f"who was {name}",
            response=f"{name} was a {title}. Notable achievements: {achieve}. {desc}",
            domain_id=2, intent_id=5, entities=[name]
        ))

    # 13. Forms of Government (Social Studies)
    govs = load_json_file("forms_of_government.json")
    for g in govs:
        name = g.get("name", "")
        defn = g.get("definition", "")
        desc = g.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is {name}",
            response=f"{name}: {defn} {desc}",
            domain_id=3, intent_id=7, entities=[name]
        ))

    # 14. Economic Systems (Social Studies)
    econs = load_json_file("economic_systems.json")
    for ec in econs:
        name = ec.get("name", "")
        defn = ec.get("definition", "")
        desc = ec.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is {name}",
            response=f"{name} is an economic doctrine. {defn} {desc}",
            domain_id=3, intent_id=7, entities=[name]
        ))

    # 15. International Organizations (Social Studies)
    orgs = load_json_file("international_organizations.json")
    for org in orgs:
        name = org.get("name", "")
        hq = org.get("headquarters", "")
        desc = org.get("description", "")
        examples.append(TrainingExample(
            prompt=f"what is {name}",
            response=f"{name} is an international institution headquartered in {hq}. {desc}",
            domain_id=3, intent_id=7, entities=[name]
        ))

    # 16. Constitutional Principles (Social Studies)
    consts = load_json_file("constitutional_principles.json")
    for cp in consts:
        name = cp.get("name", "")
        defn = cp.get("definition", "")
        purpose = cp.get("purpose", "")
        examples.append(TrainingExample(
            prompt=f"what is {name}",
            response=f"{name}: {defn} Purpose: {purpose}",
            domain_id=3, intent_id=7, entities=[name]
        ))

    # 17. World Countries Encyclopedia (Geography)
    countries = load_json_file("world_countries_encyclopedia.json")
    for c in countries:
        name = c.get("name", "")
        cap = c.get("capital", "")
        curr = c.get("currency", "")
        pop = c.get("population", 0)
        desc = c.get("overview", "")
        examples.append(TrainingExample(
            prompt=f"tell me about {name}",
            response=f"{name} is a sovereign country. Capital: {cap}, Currency: {curr}, Population: {pop:,}. {desc}",
            domain_id=1, intent_id=3, entities=[name]
        ))
        examples.append(TrainingExample(
            prompt=f"capital of {name}",
            response=f"The capital of {name} is {cap}.",
            domain_id=1, intent_id=1, entities=[name, cap]
        ))

    # 18. World Cities Encyclopedia (Geography)
    cities = load_json_file("world_cities_encyclopedia.json")
    for ci in cities:
        name = ci.get("name", "")
        country = ci.get("country", "")
        pop = ci.get("population", 0)
        desc = ci.get("description", "")
        examples.append(TrainingExample(
            prompt=f"tell me about {name}",
            response=f"{name} is a major city in {country} with an estimated population of {pop:,}. {desc}",
            domain_id=1, intent_id=0, entities=[name, country]
        ))

    return examples


class GeoMindDataset:
    """
    Dataset manager for training, fine-tuning, and evaluating GeoMind models.
    Supports synthetic data augmentation, shuffling, and file export/import.
    Includes comprehensive Wikipedia geography, history, and social studies corpora.
    """

    def __init__(self, examples: Optional[List[TrainingExample]] = None, load_wiki: bool = True):
        if examples is not None:
            self.examples = list(examples)
        else:
            self.examples = list(BASE_TRAINING_EXAMPLES)
            if load_wiki:
                wiki_examples = generate_wikipedia_training_dataset()
                self.examples.extend(wiki_examples)

    def __len__(self) -> int:
        return len(self.examples)

    def __getitem__(self, idx: int) -> TrainingExample:
        return self.examples[idx]

    def add_example(
        self,
        prompt: str,
        response: str,
        domain: Domain = Domain.GENERAL,
        intent: Intent = Intent.GENERAL_QA,
        entities: Optional[List[str]] = None
    ) -> None:
        """Adds a single training pair to the active dataset."""
        ex = TrainingExample(
            prompt=prompt,
            response=response,
            domain_id=DOMAIN_TO_ID.get(domain, 0),
            intent_id=INTENT_TO_ID.get(intent, 0),
            entities=entities or []
        )
        self.examples.append(ex)

    def augment(self) -> None:
        """
        Generates synthetic permutations to improve robustness against typos,
        abbreviations, casing, and syntactic phrasing.
        """
        augmented: List[TrainingExample] = []
        for ex in self.examples:
            # 1. Punctuation stripped and lowercased
            p_clean = ex.prompt.rstrip("?.,!").lower()
            if p_clean != ex.prompt:
                augmented.append(TrainingExample(
                    prompt=p_clean,
                    response=ex.response,
                    domain_id=ex.domain_id,
                    intent_id=ex.intent_id,
                    entities=ex.entities
                ))

            # 2. Conversational prefix variation
            prefixes = ["please tell me ", "can you explain ", "what can you tell me about "]
            for pfx in prefixes:
                if not ex.prompt.lower().startswith("what") and not ex.prompt.lower().startswith("who"):
                    augmented.append(TrainingExample(
                        prompt=pfx + ex.prompt,
                        response=ex.response,
                        domain_id=ex.domain_id,
                        intent_id=ex.intent_id,
                        entities=ex.entities
                    ))

        self.examples.extend(augmented)

    def save_json(self, filepath: str) -> None:
        """Serializes dataset to a JSON file."""
        data = [
            {
                "prompt": ex.prompt,
                "response": ex.response,
                "domain": ID_TO_DOMAIN.get(ex.domain_id, Domain.GENERAL).value,
                "intent": ID_TO_INTENT.get(ex.intent_id, Intent.GENERAL_QA).value,
                "entities": ex.entities
            }
            for ex in self.examples
        ]
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load_json(cls, filepath: str) -> "GeoMindDataset":
        """Loads a dataset from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        examples: List[TrainingExample] = []
        for item in data:
            domain = Domain(item.get("domain", "general"))
            intent = Intent(item.get("intent", "general_qa"))
            examples.append(TrainingExample(
                prompt=item["prompt"],
                response=item["response"],
                domain_id=DOMAIN_TO_ID.get(domain, 0),
                intent_id=INTENT_TO_ID.get(intent, 0),
                entities=item.get("entities", [])
            ))
        return cls(examples)
