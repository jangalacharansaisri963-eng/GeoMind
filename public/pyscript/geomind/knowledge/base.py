"""
Base classes for GeoMind knowledge sources and registries.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from geomind.core.types import Domain, Intent, QueryResult


class KnowledgeSource(ABC):
    """Abstract base class for all domain knowledge sources."""

    @property
    @abstractmethod
    def domain(self) -> Domain:
        """The primary domain handled by this source."""
        pass

    @abstractmethod
    def can_handle(self, intent: Intent, text: str) -> bool:
        """Determines if this knowledge source can satisfy the query."""
        pass

    @abstractmethod
    def query(self, intent: Intent, entities: List[str], raw_text: str, context: Optional[str] = None) -> Optional[QueryResult]:
        """Executes the query and produces a QueryResult."""
        pass
