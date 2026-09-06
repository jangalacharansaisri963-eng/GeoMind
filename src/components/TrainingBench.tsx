import React, { useState } from "react";
import { Activity, Play, CheckCircle2, TrendingDown, Award, RefreshCw, HardDrive } from "lucide-react";
import { EpochRecord, TrainingResult } from "../types";

interface TrainingBenchProps {
  onTrain: (epochs: number) => Promise<TrainingResult>;
  isTraining: boolean;
  history: EpochRecord[];
  totalParameters: number;
}

export const TrainingBench: React.FC<TrainingBenchProps> = ({
  onTrain,
  isTraining,
  history,
  totalParameters,
}) => {
  const [selectedEpochs, setSelectedEpochs] = useState<number>(3);
  const [recentResult, setRecentResult] = useState<TrainingResult | null>(null);

  const handleStartTraining = async () => {
    try {
      const res = await onTrain(selectedEpochs);
      setRecentResult(res);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 w-full space-y-8">
      {/* Training Control Center */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <Activity className="w-5 h-5 text-emerald-400" />
              <h2 className="text-xl font-bold text-slate-100">GeoMind Neural Training & Fine-Tuning Bench</h2>
            </div>
            <p className="text-sm text-slate-400 max-w-xl">
              Execute multi-epoch gradient optimization across the 18 Wikipedia datasets. Updates token embeddings and attention heads in real time.
            </p>
          </div>

          <div className="flex items-center gap-3 w-full md:w-auto">
            <div className="flex items-center bg-slate-800 p-1 rounded-xl border border-slate-700">
              {[1, 3, 5].map((ep) => (
                <button
                  key={ep}
                  onClick={() => setSelectedEpochs(ep)}
                  disabled={isTraining}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                    selectedEpochs === ep
                      ? "bg-emerald-500 text-slate-950 shadow"
                      : "text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {ep} {ep === 1 ? "Epoch" : "Epochs"}
                </button>
              ))}
            </div>

            <button
              id="start-training-button"
              onClick={handleStartTraining}
              disabled={isTraining}
              className="flex-1 md:flex-initial flex items-center justify-center gap-2 px-5 py-2.5 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-slate-950 font-bold rounded-xl text-sm transition-all shadow-lg shadow-emerald-500/20 cursor-pointer"
            >
              {isTraining ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Optimizing Gradients...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-current" />
                  <span>Train Model</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Model Weight Specifications Bar */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-800">
          <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
            <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block">Backbone</span>
            <span className="text-sm font-bold text-slate-100 font-mono">Transformer (3L, 4H)</span>
          </div>
          <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
            <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block">Neural Parameters</span>
            <span className="text-sm font-bold text-emerald-400 font-mono">{totalParameters.toLocaleString()}</span>
          </div>
          <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
            <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block">Checkpoint File</span>
            <span className="text-sm font-bold text-cyan-400 font-mono flex items-center gap-1">
              <HardDrive className="w-3.5 h-3.5" /> geomind_weights.json
            </span>
          </div>
          <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800/80">
            <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block">Loss Criterion</span>
            <span className="text-sm font-bold text-purple-400 font-mono">Cross-Entropy Multi-Head</span>
          </div>
        </div>
      </div>

      {/* Training Metrics & Progress History */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
            <TrendingDown className="w-4 h-4 text-emerald-400" />
            <span>Epoch Convergence Logs</span>
          </h3>
          <span className="text-xs text-slate-400">
            {history.length} Cumulative Epochs Recorded
          </span>
        </div>

        {history.length === 0 ? (
          <div className="py-12 text-center text-slate-500 text-sm">
            No training logs available. Click &quot;Train Model&quot; to begin neural parameter optimization.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-xs uppercase text-slate-400 bg-slate-950/60 border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4">Epoch</th>
                  <th className="py-3 px-4">Cross-Entropy Loss</th>
                  <th className="py-3 px-4">Domain Accuracy</th>
                  <th className="py-3 px-4">Intent Accuracy</th>
                  <th className="py-3 px-4">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 font-mono text-xs">
                {history.map((record, index) => (
                  <tr key={index} className="hover:bg-slate-800/40">
                    <td className="py-3 px-4 text-slate-300 font-bold">Epoch {record.epoch}</td>
                    <td className="py-3 px-4 text-amber-400">{record.loss.toFixed(4)}</td>
                    <td className="py-3 px-4 text-emerald-400 font-semibold">{record.domain_acc.toFixed(1)}%</td>
                    <td className="py-3 px-4 text-cyan-400 font-semibold">{record.intent_acc.toFixed(1)}%</td>
                    <td className="py-3 px-4">
                      <span className="inline-flex items-center gap-1 text-[11px] font-sans font-medium text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        <CheckCircle2 className="w-3 h-3" /> Saved to weights
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
