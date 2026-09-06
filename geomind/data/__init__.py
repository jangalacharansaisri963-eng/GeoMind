"""
GeoMind Built-in Datasets Package.
Contains verified Wikipedia and geographic/historical JSON datasets.
"""
import os
import json
from typing import Any, Dict, List

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def load_dataset(filename: str) -> List[Dict[str, Any]]:
    """Loads a JSON dataset file from the package data directory."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
