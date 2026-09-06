/**
 * Bridge to GeoMind's Python engine running in-browser via PyScript (see
 * index.html + public/pyscript/bridge.py).
 *
 * App.tsx's normal path is the Node/Express backend (`/api/*`, served by
 * `npm run dev` / server.ts, which shells out to geomind/server_api.py).
 * That backend doesn't exist on a static host like GitHub Pages, so App.tsx
 * falls back to these functions when the `/api/*` fetches fail. Same
 * Python engine either way — just a different transport.
 */
import type { ModelInfo, DatasetItem, TrainingResult } from "../types";

declare global {
  interface Window {
    geomindPyReady?: boolean;
    geomindPyGetModelInfo?: () => string;
    geomindPyGetDatasets?: () => string;
    geomindPyAsk?: (prompt: string) => string;
    geomindPyTrain?: (epochs: number, lr: number) => string;
  }
}

export interface PyAskResult {
  text: string;
  domain: string;
  intent: string;
  sources: string[];
  interpreted_query: string;
  confidence: number;
}

const READY_EVENT = "geomind-py-ready";
const DEFAULT_TIMEOUT_MS = 30000;

let readyPromise: Promise<void> | null = null;

/** True as soon as an HTML `<script type="py">` tag is present on the page. */
export function isPyBridgeConfigured(): boolean {
  return typeof document !== "undefined" && !!document.querySelector('script[type="py"]');
}

/**
 * Resolves once the in-browser Python engine has finished loading (Pyodide
 * boot + package/file fetch + bridge.py execution). This can take a few
 * seconds on first load. Rejects if it doesn't become ready within
 * `timeoutMs` — e.g. no `<script type="py">` tag present at all.
 */
export function waitForPyBridge(timeoutMs: number = DEFAULT_TIMEOUT_MS): Promise<void> {
  if (typeof window !== "undefined" && window.geomindPyReady) {
    return Promise.resolve();
  }
  if (!isPyBridgeConfigured()) {
    return Promise.reject(new Error("GeoMind in-browser engine is not configured on this page."));
  }
  if (readyPromise) {
    return readyPromise;
  }

  readyPromise = new Promise<void>((resolve, reject) => {
    if (window.geomindPyReady) {
      resolve();
      return;
    }
    const timer = window.setTimeout(() => {
      window.removeEventListener(READY_EVENT, onReady);
      reject(new Error("Timed out waiting for the GeoMind in-browser engine to load."));
    }, timeoutMs);

    function onReady() {
      window.clearTimeout(timer);
      window.removeEventListener(READY_EVENT, onReady);
      resolve();
    }

    window.addEventListener(READY_EVENT, onReady);
  });

  return readyPromise;
}

function parseOrThrow<T>(raw: string): T {
  const data = JSON.parse(raw);
  if (data && typeof data === "object" && "error" in data) {
    throw new Error(String((data as { error: unknown }).error));
  }
  return data as T;
}

export async function pyGetModelInfo(): Promise<ModelInfo> {
  await waitForPyBridge();
  if (!window.geomindPyGetModelInfo) throw new Error("GeoMind engine not ready");
  return parseOrThrow<ModelInfo>(window.geomindPyGetModelInfo());
}

export async function pyGetDatasets(): Promise<DatasetItem[]> {
  await waitForPyBridge();
  if (!window.geomindPyGetDatasets) throw new Error("GeoMind engine not ready");
  return parseOrThrow<DatasetItem[]>(window.geomindPyGetDatasets());
}

export async function pyAsk(prompt: string): Promise<PyAskResult> {
  await waitForPyBridge();
  if (!window.geomindPyAsk) throw new Error("GeoMind engine not ready");
  return parseOrThrow<PyAskResult>(window.geomindPyAsk(prompt));
}

export async function pyTrain(epochs: number, lr: number): Promise<TrainingResult> {
  await waitForPyBridge();
  if (!window.geomindPyTrain) throw new Error("GeoMind engine not ready");
  return parseOrThrow<TrainingResult>(window.geomindPyTrain(epochs, lr));
}
