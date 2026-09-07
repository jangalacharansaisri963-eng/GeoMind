"""
GeoMind: Independent Foundation AI Model for Geography, History, and Social Studies.
"""
from geomind.core.agent import GeoMind, ChatSession
from geomind.core.types import (
    Domain,
    Intent,
    GeoCoord,
    DistanceResult,
    QueryResult,
    Message
)
from geomind.core.session import Session
from geomind.models.geomind_model import GeoMindModel
from geomind.models.tokenizer import GeoMindTokenizer
from geomind.models.trainer import GeoMindTrainer
from geomind.models.dataset import GeoMindDataset, TrainingExample
from geomind.models.provider import GeoMindModelProvider
from geomind.models.rule_engine import RuleEngine

__version__ = "0.1.0"
__all__ = [
    "GeoMind",
    "ChatSession",
    "Domain",
    "Intent",
    "GeoCoord",
    "DistanceResult",
    "QueryResult",
    "Message",
    "Session",
    "GeoMindModel",
    "GeoMindTokenizer",
    "GeoMindTrainer",
    "GeoMindDataset",
    "TrainingExample",
    "GeoMindModelProvider",
    "RuleEngine",
    "__version__"
]
