import React from "react";
import { Globe, Cpu, Database, Activity, Sparkles } from "lucide-react";
import { ModelInfo } from "../types";

interface HeaderProps {
  activeTab: "chat" | "datasets" | "train" | "architecture";
  setActiveTab: (tab: "chat" | "datasets" | "train" | "architecture") => void;
  modelInfo: ModelInfo | null;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab, modelInfo }) => {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
              <Globe className="w-6 h-6 text-slate-950 stroke-[2.2]" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-lg text-slate-100 tracking-tight">GeoMind-1</span>
                <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                  Standalone Model
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Independent AI Model for Geography, History & Social Studies
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center space-x-1 sm:space-x-2">
            <button
              id="tab-chat"
              onClick={() => setActiveTab("chat")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "chat"
                  ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <Sparkles className="w-4 h-4" />
              <span>Inference Console</span>
            </button>

            <button
              id="tab-datasets"
              onClick={() => setActiveTab("datasets")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "datasets"
                  ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <Database className="w-4 h-4" />
              <span>Wikipedia Vault</span>
              {modelInfo && (
                <span className="ml-1 px-1.5 py-0.2 text-[10px] font-bold bg-slate-800 text-slate-300 rounded-full">
                  {modelInfo.active_datasets_count || 18}
                </span>
              )}
            </button>

            <button
              id="tab-train"
              onClick={() => setActiveTab("train")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "train"
                  ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <Activity className="w-4 h-4" />
              <span>Training Bench</span>
            </button>

            <button
              id="tab-architecture"
              onClick={() => setActiveTab("architecture")}
              className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === "architecture"
                  ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
                  : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
              }`}
            >
              <Cpu className="w-4 h-4" />
              <span>Architecture</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
  );
};
