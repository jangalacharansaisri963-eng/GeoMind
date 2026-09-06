"""
GeoMind in-browser bridge (PyScript / Pyodide).

This is what lets the exact same Python engine that powers the CLI and the
Node/Express dev server (see ../../server.ts + geomind/server_api.py) run
directly inside the visitor's browser instead — no backend required. That
matters specifically because GitHub Pages only serves static files; it can't
run a Node server or spawn a `python3` subprocess. PyScript loads a real
Python interpreter (Pyodide, compiled to WebAssembly) client-side and runs
this file once it's ready.

It intentionally reuses geomind/server_api.py's functions rather than
reimplementing them, so the static-site build and the local dev server always
answer identically.

Exposes on `window`:
    geomindPyGetModelInfo() -> JSON string
    geomindPyGetDatasets()  -> JSON string
    geomindPyAsk(prompt)    -> JSON string
    geomindPyTrain(epochs, lr) -> JSON string
    geomindPyReady          -> bool, set True once everything above is ready

Dispatches a "geomind-py-ready" event on `window` once ready, so the TS side
doesn't have to poll.
"""
import json

from js import window, CustomEvent
from pyodide.ffi import create_proxy

from geomind.server_api import (
    get_model_info,
    get_datasets_catalog,
    ask_query,
    train_model,
)


def _safe_json(fn, *args):
    """Runs fn(*args) and always returns a JSON string, error included on failure."""
    try:
        return json.dumps(fn(*args))
    except Exception as e:  # keep the browser tab alive; report the error as data
        return json.dumps({"error": str(e)})


def geomind_get_model_info():
    return _safe_json(get_model_info)


def geomind_get_datasets():
    return _safe_json(get_datasets_catalog)


def geomind_ask(prompt):
    return _safe_json(ask_query, prompt)


def geomind_train(epochs, lr):
    return _safe_json(train_model, int(epochs), float(lr))


# Expose the functions to JavaScript. create_proxy keeps the underlying
# Python callable alive for as long as `window` holds a reference to it.
window.geomindPyGetModelInfo = create_proxy(geomind_get_model_info)
window.geomindPyGetDatasets = create_proxy(geomind_get_datasets)
window.geomindPyAsk = create_proxy(geomind_ask)
window.geomindPyTrain = create_proxy(geomind_train)

window.geomindPyReady = True
window.dispatchEvent(CustomEvent.new("geomind-py-ready"))
