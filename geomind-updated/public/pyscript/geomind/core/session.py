"""
Session and conversation history management for GeoMind.
"""
import json
import time
from typing import Any, Dict, List, Optional
from geomind.core.types import Message, QueryResult, Domain, Intent


class Session:
    """Manages an interactive conversation session with history and export capabilities."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or f"session_{int(time.time())}"
        self.history: List[Message] = []
        self.created_at = time.time()
        self.last_result: Optional[QueryResult] = None

    def add_user_message(self, text: str, interpreted_query: Optional[str] = None) -> Message:
        msg = Message(
            role="user",
            content=text,
            interpreted_query=interpreted_query,
            timestamp=time.time()
        )
        self.history.append(msg)
        return msg

    def add_assistant_message(self, result: QueryResult) -> Message:
        self.last_result = result
        msg = Message(
            role="assistant",
            content=result.text,
            interpreted_query=result.interpreted_query,
            domain=result.domain,
            intent=result.intent,
            metadata=result.metadata,
            timestamp=time.time()
        )
        self.history.append(msg)
        return msg

    def clear(self) -> None:
        """Clears all conversation history."""
        self.history.clear()
        self.last_result = None

    def get_last_entity_subject(self) -> Optional[str]:
        """Returns the primary entity or subject discussed in the last turn."""
        if self.last_result and self.last_result.entities:
            # Return the primary resolved entity name
            return self.last_result.entities[0][1]
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the session to a dictionary."""
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "turn_count": len(self.history) // 2,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp,
                    "interpreted_query": m.interpreted_query,
                    "domain": m.domain.value if m.domain else None,
                    "intent": m.intent.value if m.intent else None,
                    "metadata": m.metadata
                }
                for m in self.history
            ]
        }

    def export_json(self, filepath: str) -> None:
        """Exports session history as a JSON file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    def export_markdown(self, filepath: str) -> None:
        """Exports session history as a Markdown formatted document."""
        lines = [
            f"# GeoMind Session: {self.session_id}",
            f"*Exported on {time.strftime('%Y-%m-%d %H:%M:%S')}*\n",
            "---",
            ""
        ]
        for m in self.history:
            if m.role == "user":
                lines.append(f"### 👤 User\n")
                if m.interpreted_query and m.interpreted_query != m.content:
                    lines.append(f"> *Interpreted as: {m.interpreted_query}*\n")
                lines.append(f"{m.content}\n")
            elif m.role == "assistant":
                lines.append(f"### 🌐 GeoMind\n")
                lines.append(f"{m.content}\n")
                lines.append("---\n")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
