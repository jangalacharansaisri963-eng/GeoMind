import React from "react";
import { Cpu, ShieldCheck, Zap, Globe2, Compass, Layers, GitBranch, Binary } from "lucide-react";
import { ModelInfo } from "../types";

interface ArchitectureViewProps {
  modelInfo: ModelInfo | null;
}

export const ArchitectureView: React.FC<ArchitectureViewProps> = ({ modelInfo }) => {
  return (
    <div className="max-w-5xl mx-auto px-4 py-8 w-full space-y-8">
      {/* Overview Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Cpu className="w-5 h-5 text-emerald-400" />
            <h2 className="text-xl font-bold text-slate-100">GeoMind-1 Architectural Foundation</h2>
          </div>
          <p className="text-sm text-slate-400 max-w-2xl leading-relaxed">
            A bespoke, self-contained neural-symbolic foundation model developed from scratch with no external API dependencies. Engineered specifically for geographic precision, historical causality, and constitutional social science.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 px-4 py-2.5 rounded-xl text-emerald-400 text-xs font-semibold whitespace-nowrap">
          <ShieldCheck className="w-4 h-4" />
          <span>Independent Model</span>
        </div>
      </div>

      {/* 3-Pillar Architectural Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
          <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <Layers className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-100 text-base">Neural Transformer Backbone</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Multi-layer bidirectional encoder with Multi-Head Self-Attention. Computes contextual representations across geographical and historical tokens.
          </p>
          <ul className="text-xs font-mono text-slate-300 space-y-1.5 pt-2 border-t border-slate-800">
            <li>• Layers: {modelInfo?.layers || 3}</li>
            <li>• Attention Heads: {modelInfo?.attention_heads || 4}</li>
            <li>• Hidden Dim: {modelInfo?.hidden_dimension || 64}</li>
            <li>• Intermediate Dim: {modelInfo?.intermediate_dimension || 128}</li>
            <li>• Total Parameters: {modelInfo?.total_parameters?.toLocaleString() || "148,928"}</li>
          </ul>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
          <div className="w-9 h-9 rounded-lg bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
            <Compass className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-100 text-base">Geodesic Spatial Solver</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Precision mathematical engine for spherical geometry. Computes exact Great-Circle geodesic distances using the Haversine formula and forward compass bearings.
          </p>
          <ul className="text-xs font-mono text-slate-300 space-y-1.5 pt-2 border-t border-slate-800">
            <li>• Mean Earth Radius: 6,371.0088 km</li>
            <li>• Haversine Formulation (Δσ)</li>
            <li>• Forward Azimuth Calculation (θ)</li>
            <li>• High-Precision Coordinates Index</li>
          </ul>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-3">
          <div className="w-9 h-9 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <Globe2 className="w-5 h-5" />
          </div>
          <h3 className="font-bold text-slate-100 text-base">18 Wikipedia Knowledge Vaults</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Curated encyclopedic registries covering physical landforms, global straits, historical epochs, constitutional frameworks, and sovereign nation profiles.
          </p>
          <ul className="text-xs font-mono text-slate-300 space-y-1.5 pt-2 border-t border-slate-800">
            <li>• Active Datasets: {modelInfo?.active_datasets_count || 18}</li>
            <li>• Physical, Political & Maritime</li>
            <li>• Historical Causality & Biographies</li>
            <li>• Civic Systems & International Org</li>
          </ul>
        </div>
      </div>

      {/* Inference Pipeline Diagram */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <h3 className="font-bold text-slate-100 text-base flex items-center gap-2">
          <GitBranch className="w-4 h-4 text-emerald-400" />
          <span>Inference & Grounding Pipeline</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <span className="text-[10px] font-bold text-emerald-400 uppercase">Step 1</span>
            <div className="font-semibold text-slate-200">Tokenization</div>
            <p className="text-slate-400 text-[11px]">
              Domain-specialized BPE & entity-aware subword encoding over 312-token vocabulary.
            </p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <span className="text-[10px] font-bold text-emerald-400 uppercase">Step 2</span>
            <div className="font-semibold text-slate-200">Transformer Encoder</div>
            <p className="text-slate-400 text-[11px]">
              Multi-head attention forward pass generates contextualized sequence representation.
            </p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <span className="text-[10px] font-bold text-emerald-400 uppercase">Step 3</span>
            <div className="font-semibold text-slate-200">Classification Heads</div>
            <p className="text-slate-400 text-[11px]">
              Linear projection heads output probability distributions over Domain and Intent.
            </p>
          </div>

          <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-2">
            <span className="text-[10px] font-bold text-emerald-400 uppercase">Step 4</span>
            <div className="font-semibold text-slate-200">Symbolic Grounding</div>
            <p className="text-slate-400 text-[11px]">
              Resolves verifiable coordinates, historical timelines, and mathematical distances.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
