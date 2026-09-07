import React, { useState, useEffect } from "react";
import { Header } from "./components/Header";
import { ChatConsole } from "./components/ChatConsole";
import { DatasetsVault } from "./components/DatasetsVault";
import { TrainingBench } from "./components/TrainingBench";
import { ArchitectureView } from "./components/ArchitectureView";
import { ChatMessage, ModelInfo, DatasetItem, EpochRecord, TrainingResult } from "./types";
import { pyGetModelInfo, pyGetDatasets, pyAsk, pyTrain } from "./lib/geomindPyBridge";

export default function App() {
  const [activeTab, setActiveTab] = useState<"chat" | "datasets" | "train" | "architecture">("chat");
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [datasets, setDatasets] = useState<DatasetItem[]>([]);
  const [isChatLoading, setIsChatLoading] = useState<boolean>(false);
  const [isTraining, setIsTraining] = useState<boolean>(false);
  const [trainingHistory, setTrainingHistory] = useState<EpochRecord[]>([]);

  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "init-1",
      role: "assistant",
      content:
        "Greetings! I am **GeoMind-1**, an independent, self-contained neural foundation model engineered from the ground up for **Geography, World History, and Civics/Social Studies**.\n\n" +
        "### 🌍 Model Status & Capabilities\n" +
        "- **Standalone Transformer**: 148,928 trainable parameters (4-head multi-head attention, 3 encoder layers).\n" +
        "- **18 Wikipedia Knowledge Vaults**: Indexed across global mountains, rivers, oceans, straits, historical eras, revolutions, and constitutional principles.\n" +
        "- **Precision Geodesics**: Real-time spherical great-circle calculation, bearing angles, and coordinate mapping.\n\n" +
        "Try asking me about any natural wonder, historical conflict, political system, or geographic distance!",
      domain: "system",
      intent: "greeting",
      sources: ["GeoMind-1 Neural Backbone", "Wikipedia Knowledge Vault"],
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);

  // Fetch model metadata and datasets on load
  useEffect(() => {
    fetchModelInfo();
    fetchDatasets();
  }, []);

  const fetchModelInfo = async () => {
    try {
      const res = await fetch("/api/model/info");
      if (!res.ok) throw new Error(`status ${res.status}`);
      const data = await res.json();
      setModelInfo(data);
    } catch (err) {
      // No Node/Express backend reachable (e.g. static GitHub Pages deploy) —
      // fall back to the in-browser PyScript-powered GeoMind engine.
      try {
        const data = await pyGetModelInfo();
        setModelInfo(data);
      } catch (pyErr) {
        console.error("Failed to load model info (backend and in-browser engine both unavailable):", pyErr);
      }
    }
  };

  const fetchDatasets = async () => {
    try {
      const res = await fetch("/api/datasets");
      if (!res.ok) throw new Error(`status ${res.status}`);
      const data = await res.json();
      setDatasets(data);
    } catch (err) {
      try {
        const data = await pyGetDatasets();
        setDatasets(data);
      } catch (pyErr) {
        console.error("Failed to load datasets (backend and in-browser engine both unavailable):", pyErr);
      }
    }
  };

  const handleSendMessage = async (text: string) => {
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsChatLoading(true);

    try {
      const data = await (async () => {
        try {
          const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text }),
          });
          if (!res.ok) throw new Error(`Server returned ${res.status}`);
          return await res.json();
        } catch (backendErr) {
          // No Node/Express backend reachable (e.g. static GitHub Pages
          // deploy) — fall back to the in-browser PyScript-powered engine.
          return await pyAsk(text);
        }
      })();

      const assistantMsg: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: data.text,
        domain: data.domain,
        intent: data.intent,
        sources: data.sources,
        interpreted_query: data.interpreted_query,
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err: any) {
      const errorMsg: ChatMessage = {
        id: `error-${Date.now()}`,
        role: "assistant",
        content: `Error generating response: ${err.message || "Failed to reach GeoMind engine"}`,
        domain: "system",
        intent: "error",
        sources: ["GeoMind Engine"],
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleTrain = async (epochs: number): Promise<TrainingResult> => {
    setIsTraining(true);
    try {
      const data: TrainingResult = await (async () => {
        try {
          const res = await fetch("/api/train", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ epochs }),
          });
          if (!res.ok) throw new Error(`Training failed with status ${res.status}`);
          return await res.json();
        } catch (backendErr) {
          // No Node/Express backend reachable — train in-browser instead.
          return await pyTrain(epochs, 0.02);
        }
      })();

      setTrainingHistory((prev) => [...prev, ...data.history]);
      await fetchModelInfo();
      return data;
    } finally {
      setIsTraining(false);
    }
  };

  const handleSelectQueryFromVault = (query: string) => {
    setActiveTab("chat");
    handleSendMessage(query);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-emerald-500 selection:text-slate-950">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} modelInfo={modelInfo} />

      <main className="flex-1 flex flex-col">
        {activeTab === "chat" && (
          <ChatConsole
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={isChatLoading}
          />
        )}

        {activeTab === "datasets" && (
          <DatasetsVault
            datasets={datasets}
            onSelectQuery={handleSelectQueryFromVault}
          />
        )}

        {activeTab === "train" && (
          <TrainingBench
            onTrain={handleTrain}
            isTraining={isTraining}
            history={trainingHistory}
            totalParameters={modelInfo?.total_parameters || 148928}
          />
        )}

        {activeTab === "architecture" && (
          <ArchitectureView modelInfo={modelInfo} />
        )}
      </main>
    </div>
  );
}
