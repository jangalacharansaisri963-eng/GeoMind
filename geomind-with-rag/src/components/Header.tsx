import React from "react";
import { Globe, Cpu, Database, Activity, Sparkles, Wifi, WifiOff } from "lucide-react";
import { ModelInfo } from "../types";

interface HeaderProps {
  activeTab: "chat" | "datasets" | "train" | "architecture";
  setActiveTab: (tab: "chat" | "datasets" | "train" | "architecture") => void;
  modelInfo: ModelInfo | null;
}

const TABS: { id: HeaderProps["activeTab"]; label: string; icon: React.ElementType }[] = [
  { id: "chat", label: "Inference Console", icon: Sparkles },
  { id: "datasets", label: "Knowledge Vault", icon: Database },
  { id: "train", label: "Training Bench", icon: Activity },
  { id: "architecture", label: "Architecture", icon: Cpu },
];

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab, modelInfo }) => {
  const webResearch = modelInfo?.web_research;

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 gap-3">
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-10 h-10 shrink-0 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center glow-emerald">
              <Globe className="w-6 h-6 text-slate-950 stroke-[2.2]" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg text-slate-100 tracking-tight">GeoMind-1</span>
                <span className="hidden sm:inline-block px-2 py-0.5 text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                  Standalone Model
                </span>
                {webResearch && (
                  <span
                    title={
                      webResearch.enabled
                        ? `Live web research active (${webResearch.backend})`
                        : "Live web research offline — answering from local datasets only"
                    }
                    className={`hidden md:inline-flex items-center gap-1 px-2 py-0.5 text-[11px] font-medium rounded-full border ${
                      webResearch.enabled
                        ? "bg-cyan-500/10 text-cyan-400 border-cyan-500/20"
                        : "bg-slate-800 text-slate-500 border-slate-700"
                    }`}
                  >
                    {webResearch.enabled ? <Wifi className="w-3 h-3" /> : <WifiOff className="w-3 h-3" />}
                    {webResearch.enabled ? `Live Search: ${webResearch.backend}` : "Offline Mode"}
                  </span>
                )}
              </div>
              <p className="hidden sm:block text-xs text-slate-400 truncate">
                Independent AI Model for Geography, History & Social Studies
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 overflow-x-auto no-scrollbar">
            {TABS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                id={`tab-${id}`}
                onClick={() => setActiveTab(id)}
                className={`tab-button ${activeTab === id ? "tab-active" : "tab-inactive"}`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span className="hidden sm:inline whitespace-nowrap">{label}</span>
                {id === "datasets" && modelInfo && (
                  <span className="ml-0.5 px-1.5 py-0.2 text-[10px] font-bold bg-slate-800 text-slate-300 rounded-full">
                    {modelInfo.active_datasets_count || 18}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
};
