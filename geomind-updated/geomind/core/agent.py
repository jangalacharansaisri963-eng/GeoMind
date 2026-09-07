"""
Main GeoMind AI Agent interface and high-level interaction layer.
Powered by GeoMind's independent foundation model and neural-symbolic reasoning engine.
"""
from typing import Any, Callable, Dict, List, Optional
from geomind.core.types import Domain, Intent, QueryResult, DistanceResult, GeoCoord
from geomind.core.session import Session
from geomind.knowledge.distance import compute_distance
from geomind.knowledge.geography import GeographyKnowledgeSource
from geomind.models.base import ModelProvider
from geomind.models.geomind_model import GeoMindModel
from geomind.models.provider import GeoMindModelProvider
from geomind.models.dataset import GeoMindDataset


class ChatSession:
    """Conversational chat session with memory and multi-turn context tracking."""

    def __init__(self, agent: "GeoMind", session_id: Optional[str] = None):
        self.agent = agent
        self.session = Session(session_id)

    def send(self, message: str) -> QueryResult:
        """Sends a message in the active session and returns the AI response."""
        result = self.agent.ask(
            message,
            context=[m.__dict__ for m in self.session.history]
        )
        self.session.add_user_message(message, interpreted_query=result.interpreted_query)
        self.session.add_assistant_message(result)
        return result

    @property
    def history(self) -> List[Any]:
        return self.session.history

    def clear(self) -> None:
        self.session.clear()

    def export_markdown(self, filepath: str) -> None:
        self.session.export_markdown(filepath)

    def export_json(self, filepath: str) -> None:
        self.session.export_json(filepath)


class GeoMind:
    """
    GeoMind: An independent AI foundation model focused on Geography, History, and Social Studies.
    
    Provides both high-level natural language understanding and direct analytical methods
    for distances, country profiles, historical timelines, and comparative analysis.
    """

    def __init__(
        self,
        model: Optional[GeoMindModel] = None,
        provider: Optional[ModelProvider] = None,
        checkpoint_path: Optional[str] = None
    ):
        if provider:
            self.provider = provider
            self.model = getattr(provider, "model", None)
        else:
            self.model = model or GeoMindModel(checkpoint_path=checkpoint_path)
            self.provider = GeoMindModelProvider(self.model)

        self.geo_source = GeographyKnowledgeSource()

    def ask(self, query: str, context: Optional[List[Dict[str, Any]]] = None) -> QueryResult:
        """
        Asks GeoMind a natural language question.
        
        Handles imperfect user input, spelling errors, abbreviations, and informal wording.
        """
        if not query or not query.strip():
            return QueryResult(
                text="Please provide a question about Geography, History, or Social Studies.",
                interpreted_query="",
                domain=Domain.GENERAL,
                intent=Intent.GENERAL_QA
            )
        return self.provider.generate(query.strip(), context=context)

    def start_chat(self, session_id: Optional[str] = None) -> ChatSession:
        """Initiates an interactive multi-turn conversational chat session."""
        return ChatSession(self, session_id)

    def train(
        self,
        epochs: int = 5,
        learning_rate: float = 0.02,
        dataset: Optional[GeoMindDataset] = None,
        progress_callback: Optional[Callable[[int, int, float], None]] = None,
        verbose: bool = True
    ) -> List[Dict[str, float]]:
        """
        Trains or fine-tunes GeoMind model parameters on domain datasets.
        """
        if not self.model:
            raise ValueError("Training is only available when a GeoMindModel instance is active.")
        return self.model.train(
            epochs=epochs,
            learning_rate=learning_rate,
            dataset=dataset,
            progress_callback=progress_callback,
            verbose=verbose
        )

    def save_model(self, filepath: str) -> None:
        """Saves current model weights to a file."""
        if self.model:
            self.model.save(filepath)

    def load_model(self, filepath: str) -> None:
        """Loads model weights from a file."""
        if self.model:
            self.model.load(filepath)

    def distance(self, origin: str, destination: str) -> Optional[DistanceResult]:
        """
        Calculates exact geodesic distance, bearing, and travel times between two places.
        
        Example:
            res = ai.distance("Delhi", "Mumbai")
            print(res.distance_km, res.distance_miles)
        """
        res1 = self.geo_source.resolve_location(origin)
        res2 = self.geo_source.resolve_location(destination)
        if not res1 or not res2:
            return None
        std1, coords1, _ = res1
        std2, coords2, _ = res2
        return compute_distance(std1, coords1, std2, coords2)

    def capital_of(self, country: str) -> Optional[str]:
        """Looks up the capital city of a given country."""
        res = self.geo_source.resolve_location(country)
        if res and "capital" in res[2]:
            return res[2]["capital"]
        return None

    def country(self, name: str) -> Optional[Dict[str, Any]]:
        """Retrieves structured geographic and demographic data for a country."""
        res = self.geo_source.resolve_location(name)
        if res and "capital" in res[2]:
            return res[2]
        return None

    def compare(self, subject_a: str, subject_b: str) -> QueryResult:
        """Generates a structured comparative analysis between two subjects."""
        return self.ask(f"compare {subject_a} and {subject_b}")
