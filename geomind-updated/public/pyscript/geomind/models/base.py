"""
Base ModelProvider interface for GeoMind reasoning models.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from geomind.core.types import QueryResult


class ModelProvider(ABC):
    """Abstract interface for reasoning and generation models."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The identifier of this model provider."""
        pass

    @abstractmethod
    def generate(
        self,
        query: str,
        context: Optional[List[Dict[str, Any]]] = None,
        system_instruction: Optional[str] = None
    ) -> Optional[QueryResult]:
        """Generates a structured QueryResult response."""
        pass
