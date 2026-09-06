"""
GeoMind Model Provider: Implements the ModelProvider interface for GeoMind foundation models.
"""
from typing import Any, Dict, List, Optional
from geomind.core.types import QueryResult
from geomind.models.base import ModelProvider
from geomind.models.geomind_model import GeoMindModel


class GeoMindModelProvider(ModelProvider):
    """
    Standard model provider using the GeoMind-1 standalone neural model.
    """

    def __init__(self, model: Optional[GeoMindModel] = None):
        self.model = model or GeoMindModel()

    @property
    def name(self) -> str:
        return self.model.model_name

    def generate(self, prompt: str, context: Optional[List[Dict[str, Any]]] = None) -> QueryResult:
        return self.model.generate(prompt, context=context)
