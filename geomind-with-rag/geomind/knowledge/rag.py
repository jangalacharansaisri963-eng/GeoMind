"""
Retrieval-Augmented Generation (RAG) core for GeoMind.

Designed to be fully offline-capable.  Embedding backends are tried in
order of quality:

1. sentence-transformers  (best quality, optional)
2. fastembed              (good quality, lighter, optional)
3. Pure-Python TF-IDF     (zero dependencies, always available)

The engine indexes GeoMind's built-in JSON knowledge files at startup and
can also accept extra text/markdown documents.
"""
from __future__ import annotations

import json
import math
import os
import re
import hashlib
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from geomind.core.types import Domain, Intent, QueryResult
from geomind.knowledge.rag_config import RagConfig

# ---------------------------------------------------------------------------
# Optional heavy backends (imported lazily)
# ---------------------------------------------------------------------------
_SENTENCE_TRANSFORMERS = None
_FASTEMBED = None


def _try_import_sentence_transformers():
    global _SENTENCE_TRANSFORMERS
    if _SENTENCE_TRANSFORMERS is not None:
        return _SENTENCE_TRANSFORMERS
    try:
        from sentence_transformers import SentenceTransformer
        _SENTENCE_TRANSFORMERS = SentenceTransformer
        return SentenceTransformer
    except Exception:
        _SENTENCE_TRANSFORMERS = False
        return False


def _try_import_fastembed():
    global _FASTEMBED
    if _FASTEMBED is not None:
        return _FASTEMBED
    try:
        from fastembed import TextEmbedding
        _FASTEMBED = TextEmbedding
        return TextEmbedding
    except Exception:
        _FASTEMBED = False
        return False


# ---------------------------------------------------------------------------
# Document / Chunk structures
# ---------------------------------------------------------------------------
@dataclass
class DocumentChunk:
    id: str
    text: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None


# ---------------------------------------------------------------------------
# Pure-Python TF-IDF backend (always available)
# ---------------------------------------------------------------------------
class TfidfIndex:
    """Lightweight sparse TF-IDF index with cosine similarity."""

    def __init__(self):
        self.docs: List[DocumentChunk] = []
        self.idf: Dict[str, float] = {}
        self.doc_vecs: List[Dict[str, float]] = []
        self._fitted = False

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        text = text.lower()
        # Keep alphanumerics and a few useful chars
        tokens = re.findall(r"[a-z0-9][a-z0-9\-']*", text)
        # Simple stop-word filter
        stops = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
            "of", "in", "on", "at", "to", "for", "with", "by", "from", "as",
            "and", "or", "but", "if", "then", "than", "that", "this", "these",
            "those", "it", "its", "what", "which", "who", "whom", "how", "when",
            "where", "why", "do", "does", "did", "can", "could", "would", "should",
            "about", "into", "over", "after", "before", "between", "under",
        }
        return [t for t in tokens if t not in stops and len(t) > 1]

    def fit(self, chunks: Sequence[DocumentChunk]) -> None:
        self.docs = list(chunks)
        n = len(self.docs)
        if n == 0:
            self._fitted = True
            return

        df: Counter = Counter()
        tokenized: List[List[str]] = []
        for c in self.docs:
            toks = self._tokenize(c.text)
            tokenized.append(toks)
            df.update(set(toks))

        self.idf = {
            term: math.log((n + 1) / (freq + 1)) + 1.0
            for term, freq in df.items()
        }

        self.doc_vecs = []
        for toks in tokenized:
            tf = Counter(toks)
            length = len(toks) or 1
            vec = {
                t: (cnt / length) * self.idf.get(t, 0.0)
                for t, cnt in tf.items()
            }
            self.doc_vecs.append(vec)

        self._fitted = True

    def _query_vec(self, query: str) -> Dict[str, float]:
        toks = self._tokenize(query)
        if not toks:
            return {}
        tf = Counter(toks)
        length = len(toks)
        return {
            t: (cnt / length) * self.idf.get(t, 0.0)
            for t, cnt in tf.items()
        }

    @staticmethod
    def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
        if not a or not b:
            return 0.0
        common = set(a) & set(b)
        if not common:
            return 0.0
        dot = sum(a[t] * b[t] for t in common)
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[DocumentChunk, float]]:
        if not self._fitted or not self.docs:
            return []
        qv = self._query_vec(query)
        scored = []
        for doc, dv in zip(self.docs, self.doc_vecs):
            score = self._cosine(qv, dv)
            if score > 0:
                scored.append((doc, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


# ---------------------------------------------------------------------------
# Dense embedding backends
# ---------------------------------------------------------------------------
class DenseIndex:
    """Thin wrapper around sentence-transformers or fastembed."""

    def __init__(self, backend: str, model_name: str):
        self.backend = backend
        self.model_name = model_name
        self.model = None
        self.docs: List[DocumentChunk] = []
        self.embeddings: List[List[float]] = []

    def _load(self):
        if self.model is not None:
            return
        if self.backend == "sentence-transformers":
            ST = _try_import_sentence_transformers()
            if not ST:
                raise RuntimeError("sentence-transformers not installed")
            self.model = ST(self.model_name)
        elif self.backend == "fastembed":
            FE = _try_import_fastembed()
            if not FE:
                raise RuntimeError("fastembed not installed")
            self.model = FE(model_name=self.model_name)
        else:
            raise ValueError(f"Unknown dense backend: {self.backend}")

    def fit(self, chunks: Sequence[DocumentChunk]) -> None:
        self._load()
        self.docs = list(chunks)
        texts = [c.text for c in self.docs]
        if not texts:
            self.embeddings = []
            return

        if self.backend == "sentence-transformers":
            embs = self.model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
            self.embeddings = [e.tolist() for e in embs]
        else:  # fastembed
            # fastembed returns a generator of numpy arrays
            self.embeddings = [e.tolist() for e in self.model.embed(texts)]

    @staticmethod
    def _cosine(a: List[float], b: List[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def search(self, query: str, top_k: int = 4) -> List[Tuple[DocumentChunk, float]]:
        if not self.docs or not self.embeddings:
            return []
        self._load()
        if self.backend == "sentence-transformers":
            q_emb = self.model.encode([query], normalize_embeddings=True)[0].tolist()
        else:
            q_emb = next(self.model.embed([query])).tolist()

        scored = []
        for doc, emb in zip(self.docs, self.embeddings):
            score = self._cosine(q_emb, emb)
            scored.append((doc, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


# ---------------------------------------------------------------------------
# Document loading helpers
# ---------------------------------------------------------------------------
_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= chunk_size:
        return [text] if text else []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if end >= len(text):
            break
    return chunks


def _json_to_text(obj: Any, prefix: str = "") -> List[str]:
    """Flatten a JSON object into readable text snippets."""
    snippets = []
    if isinstance(obj, dict):
        # Prefer human-friendly fields
        name = obj.get("name") or obj.get("title") or obj.get("official_name")
        parts = []
        if name:
            parts.append(str(name))
        for key in (
            "capital", "continent", "region", "population", "area_sq_km",
            "currency", "languages", "borders", "overview", "description",
            "summary", "causes", "consequences", "achievements", "impact",
            "definition", "principles", "features", "major_features",
        ):
            if key in obj and obj[key]:
                val = obj[key]
                if isinstance(val, list):
                    val = ", ".join(str(v) for v in val)
                parts.append(f"{key.replace('_', ' ')}: {val}")
        if parts:
            snippets.append(". ".join(parts))
        # Recurse into nested structures if useful
        for k, v in obj.items():
            if k in ("coords", "coordinates", "aliases"):
                continue
            if isinstance(v, (dict, list)) and k not in (
                "capital", "borders", "languages", "major_features"
            ):
                snippets.extend(_json_to_text(v, prefix=f"{prefix}{k}."))
    elif isinstance(obj, list):
        for item in obj:
            snippets.extend(_json_to_text(item, prefix))
    return snippets


def load_builtin_chunks(chunk_size: int = 650, overlap: int = 80) -> List[DocumentChunk]:
    """Turn every JSON file in geomind/data into searchable chunks."""
    chunks: List[DocumentChunk] = []
    if not _DATA_DIR.exists():
        return chunks

    for path in sorted(_DATA_DIR.glob("*.json")):
        # Skip the large weights file
        if path.name == "geomind_weights.json":
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        texts = _json_to_text(data)
        for i, raw in enumerate(texts):
            for j, piece in enumerate(_chunk_text(raw, chunk_size, overlap)):
                cid = hashlib.md5(f"{path.name}:{i}:{j}:{piece[:40]}".encode()).hexdigest()[:12]
                chunks.append(
                    DocumentChunk(
                        id=cid,
                        text=piece,
                        source=path.name,
                        metadata={"file": path.name, "index": i},
                    )
                )
    return chunks


def load_extra_documents(
    paths: Sequence[str],
    chunk_size: int = 650,
    overlap: int = 80,
) -> List[DocumentChunk]:
    chunks: List[DocumentChunk] = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            continue
        if path.is_dir():
            files = list(path.rglob("*.txt")) + list(path.rglob("*.md"))
        else:
            files = [path]
        for fp in files:
            try:
                text = fp.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for j, piece in enumerate(_chunk_text(text, chunk_size, overlap)):
                cid = hashlib.md5(f"{fp}:{j}:{piece[:40]}".encode()).hexdigest()[:12]
                chunks.append(
                    DocumentChunk(
                        id=cid,
                        text=piece,
                        source=str(fp.name),
                        metadata={"file": str(fp)},
                    )
                )
    return chunks


# ---------------------------------------------------------------------------
# Main RAG Engine
# ---------------------------------------------------------------------------
class RagEngine:
    """
    Offline RAG engine for GeoMind.

    Usage:
        engine = RagEngine()          # uses RagConfig.from_env()
        if engine.is_available():
            result = engine.query("causes of the French Revolution")
    """

    def __init__(self, config: Optional[RagConfig] = None):
        self.config = config or RagConfig.from_env()
        self._index = None          # TfidfIndex or DenseIndex
        self._backend_name = "none"
        self._ready = False
        self._init_error: Optional[str] = None

        if self.config.enabled:
            try:
                self._build_index()
            except Exception as e:
                self._init_error = str(e)
                self._ready = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def is_available(self) -> bool:
        return bool(self.config.enabled and self._ready and self._index is not None)

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.config.enabled,
            "ready": self._ready,
            "backend": self._backend_name,
            "num_chunks": len(getattr(self._index, "docs", [])) if self._index else 0,
            "error": self._init_error,
        }

    def query(self, query: str) -> Optional[QueryResult]:
        if not self.is_available():
            return None
        if len(query.split()) < self.config.min_query_words:
            return None

        hits = self._index.search(query, top_k=self.config.top_k)
        # Filter by minimum score
        hits = [(c, s) for c, s in hits if s >= self.config.min_score]
        if not hits:
            return None

        # Build context string
        context_parts = []
        sources = []
        total_len = 0
        for chunk, score in hits:
            snippet = chunk.text.strip()
            if total_len + len(snippet) > self.config.max_context_chars:
                break
            context_parts.append(f"• {snippet}")
            total_len += len(snippet)
            if chunk.source not in sources:
                sources.append(chunk.source)

        if not context_parts:
            return None

        context_block = "\n\n".join(context_parts)

        if self.config.synthesize_answer:
            text = self._synthesize(query, context_block, sources)
        else:
            text = (
                f"{self.config.answer_prefix}"
                f"**Retrieved context for:** *{query}*\n\n"
                f"{context_block}"
            )

        return QueryResult(
            text=text,
            interpreted_query=query,
            domain=Domain.GENERAL,
            intent=Intent.GENERAL_QA,
            entities=[],
            metadata={
                "rag_backend": self._backend_name,
                "rag_hits": len(hits),
                "rag_scores": [round(s, 3) for _, s in hits],
            },
            sources=sources or ["GeoMind RAG"],
            confidence=min(1.0, hits[0][1] + 0.15) if hits else 0.5,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _choose_backend(self) -> str:
        requested = (self.config.embedding_backend or "auto").lower().strip()
        if requested == "tfidf":
            return "tfidf"
        if requested == "sentence-transformers":
            if _try_import_sentence_transformers():
                return "sentence-transformers"
            return "tfidf"
        if requested == "fastembed":
            if _try_import_fastembed():
                return "fastembed"
            return "tfidf"
        # auto
        if _try_import_sentence_transformers():
            return "sentence-transformers"
        if _try_import_fastembed():
            return "fastembed"
        return "tfidf"

    def _build_index(self) -> None:
        chunks: List[DocumentChunk] = []
        if self.config.index_builtin_json:
            chunks.extend(
                load_builtin_chunks(
                    chunk_size=self.config.chunk_size,
                    overlap=self.config.chunk_overlap,
                )
            )
        if self.config.extra_document_paths:
            chunks.extend(
                load_extra_documents(
                    self.config.extra_document_paths,
                    chunk_size=self.config.chunk_size,
                    overlap=self.config.chunk_overlap,
                )
            )

        if not chunks:
            self._init_error = "No documents to index"
            self._ready = False
            return

        backend = self._choose_backend()
        self._backend_name = backend

        if backend == "tfidf":
            index = TfidfIndex()
            index.fit(chunks)
            self._index = index
        else:
            index = DenseIndex(backend=backend, model_name=self.config.embedding_model)
            index.fit(chunks)
            self._index = index

        self._ready = True

    def _synthesize(self, query: str, context: str, sources: List[str]) -> str:
        """
        Lightweight extractive synthesis.
        We deliberately avoid calling an external LLM so the system stays
        offline and dependency-free.  A future version can plug in a local
        LLM here when available.
        """
        # Take the highest-scoring snippets and present them cleanly
        header = self.config.answer_prefix
        body = (
            f"Based on GeoMind's local knowledge base, here is the most relevant "
            f"information for your question:\n\n"
            f"**Question:** {query}\n\n"
            f"{context}\n\n"
        )
        if sources:
            src_line = "Sources: " + ", ".join(sources)
            body += f"*{src_line}*"
        return header + body


# Convenience singleton used by RuleEngine
_default_engine: Optional[RagEngine] = None


def get_rag_engine(config: Optional[RagConfig] = None) -> RagEngine:
    global _default_engine
    if config is not None:
        return RagEngine(config)
    if _default_engine is None:
        _default_engine = RagEngine()
    return _default_engine
