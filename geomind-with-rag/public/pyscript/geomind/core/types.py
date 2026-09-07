"""
Core data types and structures for GeoMind.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
import time


class Domain(str, Enum):
    GEOGRAPHY = "geography"
    HISTORY = "history"
    SOCIAL_STUDIES = "social_studies"
    DISTANCE = "distance"
    COMPARISON = "comparison"
    GENERAL = "general"


class Intent(str, Enum):
    DISTANCE_CALCULATION = "distance_calculation"
    CAPITAL_LOOKUP = "capital_lookup"
    COUNTRY_INFO = "country_info"
    CITY_INFO = "city_info"
    LOCATION_COORDINATES = "location_coordinates"
    HISTORICAL_EVENT = "historical_event"
    HISTORICAL_FIGURE = "historical_figure"
    CAUSE_AND_CONSEQUENCE = "cause_and_consequence"
    COMPARISON = "comparison"
    DEFINITION = "definition"
    POPULATION_QUERY = "population_query"
    BORDERING_COUNTRIES = "bordering_countries"
    CURRENCY_LOOKUP = "currency_lookup"
    GENERAL_QA = "general_qa"
    GREETING = "greeting"
    WEB_RESEARCH = "web_research"
    RAG = "rag"


@dataclass
class GeoCoord:
    """Geographic coordinate pair (Latitude, Longitude)."""
    lat: float
    lon: float

    def __repr__(self) -> str:
        lat_str = f"{abs(self.lat):.4f}°{'N' if self.lat >= 0 else 'S'}"
        lon_str = f"{abs(self.lon):.4f}°{'E' if self.lon >= 0 else 'W'}"
        return f"{lat_str}, {lon_str}"


@dataclass
class DistanceResult:
    """Calculated geographic distance between two entities."""
    origin_name: str
    destination_name: str
    origin_coords: GeoCoord
    destination_coords: GeoCoord
    distance_km: float
    distance_miles: float
    bearing_degrees: float
    compass_direction: str
    flight_time_hours: float
    driving_time_hours: Optional[float] = None
    context: str = ""


@dataclass
class Message:
    """A message in a conversational session."""
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: float = field(default_factory=time.time)
    interpreted_query: Optional[str] = None
    domain: Optional[Domain] = None
    intent: Optional[Intent] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResult:
    """The result returned by GeoMind's reasoning engine."""
    text: str
    interpreted_query: str
    domain: Domain
    intent: Intent
    entities: List[Tuple[str, str]] = field(default_factory=list)  # (original, resolved)
    metadata: Dict[str, Any] = field(default_factory=dict)
    sources: List[str] = field(default_factory=list)
    confidence: float = 1.0

    def __str__(self) -> str:
        return self.text
