"""
RAG configuration for GeoMind.

All settings are overridable via environment variables or by passing a
custom RagConfig instance to RagEngine.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RagConfig:
    """Configuration for the Retrieval-Augmented Generation layer."""

    # ------------------------------------------------------------------
    # Feature flags
    # ------------------------------------------------------------------
    enabled: bool = True

    # Minimum number of words in a query before RAG is considered
    min_query_words: int = 3

    # How many chunks to retrieve
    top_k: int = 4

    # Minimum similarity score (0.0 – 1.0) to keep a chunk
    # Lower values = more recall, higher = more precision
    min_score: float = 0.18

    # Maximum characters returned in the final context block
    max_context_chars: int = 2200

    # ------------------------------------------------------------------
    # Embedding / retrieval backend
    # ------------------------------------------------------------------
    # "auto" tries: sentence-transformers → fastembed → pure-python TF-IDF
    # You can force one of: "sentence-transformers", "fastembed", "tfidf"
    embedding_backend: str = "auto"

    # Model name used when sentence-transformers or fastembed is available
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # ------------------------------------------------------------------
    # Document sources
    # ------------------------------------------------------------------
    # Whether to automatically index the built-in JSON knowledge files
    index_builtin_json: bool = True

    # Extra plain-text / markdown files or directories to index (absolute or
    # relative to the package data directory). Empty by default.
    extra_document_paths: List[str] = field(default_factory=list)

    # Chunk size (characters) when splitting long documents
    chunk_size: int = 650
    chunk_overlap: int = 80

    # ------------------------------------------------------------------
    # Generation / answer style
    # ------------------------------------------------------------------
    # If True, the engine produces a short natural-language answer from the
    # retrieved context. If False it only returns the raw context snippets.
    synthesize_answer: bool = True

    # Prefix shown to the user when RAG answers
    answer_prefix: str = "📚 **GeoMind Knowledge Retrieval (RAG)**\n\n"

    @classmethod
    def from_env(cls) -> "RagConfig":
        """Build a config, honouring common environment variables."""
        def _bool(name: str, default: bool) -> bool:
            val = os.environ.get(name)
            if val is None:
                return default
            return val.strip().lower() in ("1", "true", "yes", "on")

        def _int(name: str, default: int) -> int:
            val = os.environ.get(name)
            try:
                return int(val) if val is not None else default
            except ValueError:
                return default

        def _float(name: str, default: float) -> float:
            val = os.environ.get(name)
            try:
                return float(val) if val is not None else default
            except ValueError:
                return default

        return cls(
            enabled=_bool("GEOMIND_RAG_ENABLED", True),
            min_query_words=_int("GEOMIND_RAG_MIN_WORDS", 3),
            top_k=_int("GEOMIND_RAG_TOP_K", 4),
            min_score=_float("GEOMIND_RAG_MIN_SCORE", 0.18),
            max_context_chars=_int("GEOMIND_RAG_MAX_CONTEXT", 2200),
            embedding_backend=os.environ.get("GEOMIND_RAG_BACKEND", "auto"),
            embedding_model=os.environ.get(
                "GEOMIND_RAG_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
            ),
            index_builtin_json=_bool("GEOMIND_RAG_INDEX_JSON", True),
            synthesize_answer=_bool("GEOMIND_RAG_SYNTHESIZE", True),
        )
