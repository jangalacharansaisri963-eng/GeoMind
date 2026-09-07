# GeoMind 🌍

**GeoMind** (`geomind-ai`) is an independent foundation AI model focused on **Geography, History, and Social Studies**.

GeoMind operates as a standalone foundation model (`GeoMind-1`) with its own neural transformer architecture, tokenization engine, parameters, datasets, and training pipeline—built in pure Python without reliance on external commercial model APIs.

[![PyPI version](https://img.shields.io/badge/pypi-geomind--ai-blue.svg)](https://pypi.org/project/geomind-ai/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

---

## 🧠 GeoMind-1 Model Architecture

GeoMind is built as an independent, domain-specialized foundation model:

- **Model Type**: Pure-Python Neural Transformer with Multi-Head Self-Attention and Multi-Task Reasoning Heads.
- **Trainable Parameters**: ~110,000+ trainable parameters across token embeddings, sinusoidal positional encodings, self-attention projection matrices ($W_q, W_k, W_v, W_o$), feed-forward layers, and multi-task prediction heads.
- **Tokenizer**: `GeoMindTokenizer` with subword fragmentation, special domain control tokens (`<geo>`, `<hist>`, `<soc>`, `<query>`, `<thought>`, `<response>`), and typo-tolerant encoding.
- **Training Pipeline**: Built-in `GeoMindTrainer` supporting supervised domain fine-tuning, learning rate scheduling, cross-entropy loss optimization, and parameter checkpointing.
- **Datasets**: Curated Geography, History, and Social Studies datasets with synthetic data augmentation.
- **Factual Precision**: Grounded symbolic decoding layer ensuring accurate geodesic calculations, dates, capitals, and civics definitions.

---

## ✨ Features

- **🌐 Core Domains**:
  - **Geography**: Countries, capitals, coordinates, populations, borders, currencies, landforms, and world cities.
  - **Distances & Routing**: Exact geodesic Haversine distance calculations (km & miles), compass bearings, cardinal directions, flight durations, and driving approximations.
  - **History**: Key eras, world wars, revolutions, ancient civilizations, timelines, and biographical profiles of pivotal historical figures.
  - **Causes & Consequences**: In-depth analysis of the underlying root catalysts and long-term societal, political, and economic impacts of major historical events.
  - **Social Studies & Civics**: Definitions and deep-dives into forms of government, economic models (capitalism, socialism), constitutional principles (separation of powers, federalism), and human geography.
  - **Comparative Analysis**: Instant side-by-side comparative matrices across countries, cities, historical events, and social ideologies.

- **🔤 Robust NLP & Typo Tolerance**:
  - Automatically recognizes and corrects spelling errors, phonetic variations, transpositions, and abbreviations.
  - Handles queries like `"ditace between delhi & mumbi"` as `"distance between Delhi and Mumbai"`, or `"captial of fance"` as `"capital of France"`.

- **💻 Polished AI CLI**:
  - Interactive multi-turn conversation mode with session history and formatted Markdown rendering.
  - Model management commands: `/model` (architecture & parameter inspection) and `/train` (interactive fine-tuning).
  - Utility slash commands: `/help`, `/history`, `/clear`, `/info`, `/stats`, `/export`, `/distance`, `/compare`.
  - Seamless one-shot execution and UNIX pipeline support: `echo "What is federalism?" | geomind`.

- **🧩 Python API & Model Customization**:
  - Clean, intuitive Python API.
  - Train model on custom datasets: `ai.train(epochs=10, learning_rate=0.01)`.
  - Save and load model checkpoints: `ai.save_model("weights.json")`.
  - Zero required external dependencies for core functionality.

---

## 🚀 Installation

Install the package from PyPI:

```bash
pip install geomind-ai
```

To enable enhanced rich terminal styling:

```bash
pip install "geomind-ai[cli]"
```

For development and local testing:

```bash
git clone https://github.com/geomind-ai/geomind.git
cd geomind
pip install -e ".[test,cli]"
```

---

## 🖥️ Command-Line Interface (CLI)

### Interactive Conversation Mode

Launch the interactive CLI by running:

```bash
geomind
```

Inside the session, you can ask questions or use slash commands:

```text
geomind > ditace between delhi & mumbi
💡 Interpreted as: "distance between Delhi and Mumbai"

The great-circle geodesic distance between Delhi and Mumbai is approximately 1,148.1 km (713.4 miles).
Bearing: 203.5° (South-Southwest)
Estimated Flight Time: ~1.4 hours

geomind > /model
🧠 GeoMind-1 Model Architecture
- Total Parameters: 110,000+
- Layers: 3 Transformer blocks
- Attention Heads: 4
- Vocabulary Size: 180+ tokens
- Specialized Domains: Geography, History, Social Studies

geomind > /train 5
Starting GeoMind-1 neural training (5 epochs)...
Training model weights... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
✓ Training complete! Parameters tuned.
```

### CLI Options

```bash
# Display model specifications and parameter count
geomind --model-info

# Train / fine-tune model from CLI
geomind --train --epochs 10 --lr 0.01

# Train on custom dataset file
geomind --train --dataset my_dataset.json --epochs 5

# One-shot query
geomind "causes and consequences of World War 1"

# Pipe input through stdin
echo "compare capitalism and socialism" | geomind

# Export response to Markdown
geomind "tell me about Japan" --export japan.md
```

---

## 🐍 Python API

### Basic Usage

```python
from geomind import GeoMind

# Initialize GeoMind with GeoMind-1 foundation model
ai = GeoMind()

# Natural language query (handles typos & abbreviations)
result = ai.ask("ditace between delhi & mumbi")
print(result.text)
print(f"Interpreted: {result.interpreted_query}")
print(f"Domain: {result.domain.value}")
```

### Multi-Turn Chat Sessions

```python
chat = ai.start_chat()

# First turn
res1 = chat.send("What is the capital of France?")
print(res1.text)

# Context-aware follow-up
res2 = chat.send("What is its population?")
print(res2.text)

# Export conversation session
chat.export_markdown("session_history.md")
```

### Model Training & Fine-Tuning

```python
from geomind import GeoMind, GeoMindDataset

ai = GeoMind()

# Inspect model info
print(ai.model.get_info())

# Fine-tune GeoMind-1 on custom training examples
history = ai.train(epochs=5, learning_rate=0.02)
for epoch_stat in history:
    print(epoch_stat)

# Save and load model checkpoints
ai.save_model("my_geomind_weights.json")
ai.load_model("my_geomind_weights.json")
```

### Direct Analytical Methods

```python
# Geodesic distance calculation
dist = ai.distance("Delhi", "Mumbai")
print(f"Distance: {dist.distance_km:.1f} km ({dist.distance_miles:.1f} miles)")
print(f"Bearing: {dist.bearing_degrees:.1f}° ({dist.compass_direction})")

# Capital lookup
print(ai.capital_of("Japan"))  # Tokyo

# Structured country profile
country_info = ai.country("Germany")
print(country_info["capital"], country_info["currency"], country_info["borders"])

# Comparative analysis
comparison = ai.compare("capitalism", "socialism")
print(comparison.text)
```

---

## 🚢 Deploying as a Static Site (GitHub Pages)

The frontend (`src/`) can run with **zero backend**, deployable straight to GitHub Pages:

- **In-browser Python engine**: `public/pyscript/` bundles the entire `geomind` package and loads it client-side via [PyScript](https://pyscript.net) (Pyodide/WebAssembly) — see `public/pyscript/bridge.py`. No server, no subprocess.
- **Automatic fallback**: `src/lib/geomindPyBridge.ts` is used by `App.tsx` whenever the `/api/*` routes (normally served by `server.ts` + `geomind/server_api.py` during local dev) aren't reachable — exactly the case on a static host.
- **Unified CI/CD Pipeline** (`.github/workflows/ci-cd.yml`):
  - **Stage 1 (every push)**: Runs Python test suite to validate engine integrity.
  - **Stage 2 (every push)**: Builds frontend with Vite.
  - **Stage 3 (main branch only)**: Auto-deploys to GitHub Pages. One-time setup: repo **Settings → Pages → Source → GitHub Actions**.
  - **Stage 4 (weekly Sundays or manual trigger)**: Retrains GeoMind-1 checkpoint, smoke-tests Playwright web research, commits checkpoint if changed. All on a real Ubuntu runner where glibc/Playwright actually work (unlike Termux/Android).

Local dev (`npm run dev`) keeps working exactly as before, using the Node/Python bridge. The PyScript path only kicks in when that bridge is absent.

---

## 🔎 Optional: Live Web Research (Playwright)

For questions outside GeoMind's local datasets, `geomind/knowledge/web_research.py` can optionally drive a real, unmodified Chromium browser via [Playwright](https://playwright.dev/python/) to run a live search and summarize the results. It's fully optional and fails gracefully — GeoMind falls back to its normal offline response if Playwright/a browser isn't available.

```bash
pip install "geomind-ai[research]"
python -m playwright install chromium
```

**Note:** Playwright's browser binaries require a standard glibc-based OS (Linux/macOS/Windows). They are not installable on Termux/Android, since Termux runs on Bionic libc. On Termux, `web_research.is_available()` simply returns `False` and GeoMind uses its offline datasets as usual — this feature is best run on a laptop or in CI (see `research-and-train.yml` above).

---

## 🧪 Testing

Run the comprehensive unit test suite (47 tests):

```bash
pytest -v
```

---



---

## 📚 Offline RAG (Retrieval-Augmented Generation)

GeoMind now includes a built-in **offline RAG core** that retrieves relevant
chunks from its local knowledge base before falling back to web search.

### How it works

1. Structured knowledge sources (capitals, events, etc.) are still tried first.
2. If no exact match is found, the **RAG engine** searches the indexed JSON
   knowledge files using TF-IDF (zero dependencies) or optional dense
   embeddings (`sentence-transformers` / `fastembed`).
3. Only if RAG also finds nothing does GeoMind attempt live web research
   (Google Custom Search or Playwright).

### Configuration (environment variables)

| Variable | Default | Meaning |
|----------|---------|---------|
| `GEOMIND_RAG_ENABLED` | `true` | Turn RAG on/off |
| `GEOMIND_RAG_BACKEND` | `auto` | `auto` / `tfidf` / `sentence-transformers` / `fastembed` |
| `GEOMIND_RAG_TOP_K` | `4` | Number of chunks to retrieve |
| `GEOMIND_RAG_MIN_SCORE` | `0.18` | Minimum similarity threshold |
| `GEOMIND_RAG_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Dense model name |

### Optional better embeddings

```bash
pip install "geomind-ai[rag]"
# or
pip install sentence-transformers
```

Without any extra packages the pure-Python TF-IDF backend is used automatically
and works fully offline.

### Programmatic use

```python
from geomind.knowledge.rag import get_rag_engine, RagConfig

engine = get_rag_engine()
print(engine.status())

result = engine.query("causes of World War 1")
if result:
    print(result.text)
```

## 📄 License

Distributed under the **Apache 2.0 License**. See [LICENSE](LICENSE) for details.
