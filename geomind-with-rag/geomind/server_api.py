"""
Bridge API helper for GeoMind web application interface.
Exposes JSON endpoints for model inference, inspection, dataset cataloging, and training.
"""
import sys
import os
import json
from typing import Any, Dict, List

# Ensure geomind package is accessible
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from geomind.core.agent import GeoMind
from geomind.models.geomind_model import GeoMindModel
from geomind.models.dataset import GeoMindDataset
from geomind.knowledge.web_research import WebResearchEngine
from geomind.knowledge.rag import get_rag_engine


def _web_research_status() -> Dict[str, Any]:
    engine = WebResearchEngine()
    if engine._google_configured():
        return {"enabled": True, "backend": "google"}
    if engine._playwright_available():
        return {"enabled": True, "backend": "playwright"}
    return {"enabled": False, "backend": None}


def get_model_info() -> Dict[str, Any]:
    model = GeoMindModel()
    info = model.get_info()
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    dataset_files = [f for f in os.listdir(data_dir) if f.endswith(".json") and f != "geomind_weights.json"]
    info["active_datasets_count"] = len(dataset_files)
    info["datasets"] = dataset_files
    info["web_research"] = _web_research_status()
    try:
        info["rag"] = get_rag_engine().status()
    except Exception as e:
        info["rag"] = {"error": str(e)}
    return info


def get_datasets_catalog() -> List[Dict[str, Any]]:
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    datasets = []
    category_map = {
        "mountains.json": ("Physical Geography", "World Mountains & Peaks (Himalayas, Andes, Rockies, Alps)"),
        "rivers.json": ("Physical Geography", "Major Global River Systems (Nile, Amazon, Yangtze, Danube)"),
        "oceans_seas.json": ("Physical Geography", "World Oceans, Marginal Seas, and Mariana Trench"),
        "deserts.json": ("Physical Geography", "Arid & Polar Deserts (Sahara, Gobi, Atacama, Antarctica)"),
        "islands.json": ("Physical Geography", "Continental & Volcanic Islands (Greenland, Borneo, Madagascar)"),
        "lakes.json": ("Physical Geography", "Major Freshwater & Saline Lakes (Baikal, Caspian, Superior)"),
        "straits_and_canals.json": ("Maritime & Strategic", "Global Chokepoints (Strait of Malacca, Suez Canal, Panama Canal)"),
        "world_wonders_landmarks.json": ("Landmarks & Heritage", "Ancient & Modern Wonders (Pyramids, Taj Mahal, Colosseum)"),
        "geographical_extremes.json": ("Earth Extremes", "Poles of Inaccessibility, Highest, Deepest, Hottest Places"),
        "world_countries_encyclopedia.json": ("Political Geography", "Sovereign States, Capitals, Populations & Borders"),
        "world_cities_encyclopedia.json": ("Urban Geography", "Major Global Metropolises, Coordinates & Elevation"),
        "historical_eras.json": ("World History", "Epochs & Transformations (Renaissance, Industrial Revolution, Pax Romana)"),
        "historical_events.json": ("World History", "Pivotal Global Conflicts, Treaties & Revolutions"),
        "historical_figures.json": ("World History", "Influential Philosophers, Leaders, Diplomats & Scientists"),
        "forms_of_government.json": ("Social Studies & Civics", "Constitutional Monarchies, Republics, Parliamentary Systems"),
        "economic_systems.json": ("Social Studies & Civics", "Market Economies, Command, Mixed, Mercantilism"),
        "international_organizations.json": ("International Relations", "United Nations, WHO, WTO, NATO, ASEAN"),
        "constitutional_principles.json": ("Legal & Political Philosophy", "Separation of Powers, Federalism, Judicial Review, Rule of Law")
    }

    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith(".json") and filename != "geomind_weights.json":
            path = os.path.join(data_dir, filename)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    count = len(data) if isinstance(data, list) else 1
            except Exception:
                count = 0
            
            cat, desc = category_map.get(filename, ("General Knowledge", "Domain dataset"))
            datasets.append({
                "filename": filename,
                "category": cat,
                "description": desc,
                "item_count": count
            })
    return datasets


def ask_query(prompt: str) -> Dict[str, Any]:
    ai = GeoMind()
    result = ai.ask(prompt)
    return {
        "text": result.text,
        "domain": result.domain.value,
        "intent": result.intent.value,
        "sources": result.sources,
        "interpreted_query": result.interpreted_query,
        "confidence": getattr(result, "confidence", 0.98)
    }


def train_model(epochs: int = 3, lr: float = 0.02) -> Dict[str, Any]:
    model = GeoMindModel()
    history = model.train(epochs=epochs, learning_rate=lr, verbose=False)
    weights_path = os.path.join(os.path.dirname(__file__), "data", "geomind_weights.json")
    model.save(weights_path)
    return {
        "status": "success",
        "epochs_trained": len(history),
        "history": history,
        "checkpoint_path": weights_path,
        "total_parameters": model.total_parameters
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No action specified"}))
        sys.exit(1)

    action = sys.argv[1]

    try:
        if action == "info":
            print(json.dumps(get_model_info()))
        elif action == "datasets":
            print(json.dumps(get_datasets_catalog()))
        elif action == "ask":
            prompt = sys.argv[2] if len(sys.argv) > 2 else ""
            print(json.dumps(ask_query(prompt)))
        elif action == "train":
            epochs = int(sys.argv[2]) if len(sys.argv) > 2 else 3
            lr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
            print(json.dumps(train_model(epochs, lr)))
        else:
            print(json.dumps({"error": f"Unknown action: {action}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
