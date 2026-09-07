import React, { useState } from "react";
import { Database, Search, Layers, FileText, ArrowUpRight, CheckCircle2 } from "lucide-react";
import { DatasetItem } from "../types";

interface DatasetsVaultProps {
  datasets: DatasetItem[];
  onSelectQuery: (query: string) => void;
}

export const DatasetsVault: React.FC<DatasetsVaultProps> = ({ datasets, onSelectQuery }) => {
  const [filter, setFilter] = useState<string>("All");
  const [search, setSearch] = useState<string>("");

  const categories = ["All", ...Array.from(new Set(datasets.map((d) => d.category)))];

  const filteredDatasets = datasets.filter((d) => {
    const matchesCategory = filter === "All" || d.category === filter;
    const matchesSearch =
      d.filename.toLowerCase().includes(search.toLowerCase()) ||
      d.description.toLowerCase().includes(search.toLowerCase()) ||
      d.category.toLowerCase().includes(search.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const totalItems = datasets.reduce((acc, d) => acc + d.item_count, 0);

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 w-full space-y-6">
      {/* Header Metric Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Database className="w-5 h-5 text-emerald-400" />
            <h2 className="text-xl font-bold text-slate-100">Wikipedia Knowledge & Geography Vault</h2>
          </div>
          <p className="text-sm text-slate-400 max-w-2xl">
            Expanded foundation datasets curated from verified Wikipedia encyclopedias, geographic registries, and historical archives.
          </p>
        </div>
        <div className="flex items-center gap-4 bg-slate-950/60 px-5 py-3 rounded-xl border border-slate-800">
          <div>
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block">Datasets</span>
            <span className="text-2xl font-black text-emerald-400">{datasets.length} Active</span>
          </div>
          <div className="w-px h-8 bg-slate-800" />
          <div>
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wider block">Knowledge Records</span>
            <span className="text-2xl font-black text-cyan-400">{totalItems} Verified</span>
          </div>
        </div>
      </div>

      {/* Filters & Search */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto pb-1 no-scrollbar">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all cursor-pointer whitespace-nowrap ${
                filter === cat
                  ? "bg-emerald-500 text-slate-950 font-semibold"
                  : "bg-slate-800 text-slate-300 hover:bg-slate-700"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Search */}
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search datasets or records..."
            className="w-full pl-9 pr-3 py-2 bg-slate-800 text-slate-100 placeholder-slate-400 text-xs rounded-lg border border-slate-700 focus:outline-none focus:border-emerald-500"
          />
        </div>
      </div>

      {/* Grid of Datasets */}
      {filteredDatasets.length === 0 ? (
        <div className="py-16 text-center text-slate-500 text-sm">
          No datasets match "{search}" in {filter}. Try a different search or category.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredDatasets.map((ds, idx) => (
            <div
              key={idx}
              className="card-hover p-5 flex flex-col justify-between fade-in group"
            >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold tracking-wide uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                  {ds.category}
                </span>
                <span className="text-xs font-mono text-cyan-400 bg-cyan-950/40 px-2 py-0.5 rounded border border-cyan-800/40">
                  {ds.item_count} items
                </span>
              </div>

              <h3 className="font-semibold text-slate-100 text-sm group-hover:text-emerald-300 transition-colors flex items-center gap-1.5 font-mono">
                <FileText className="w-4 h-4 text-slate-400" />
                {ds.filename}
              </h3>

              <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                {ds.description}
              </p>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
              <span className="text-[11px] text-slate-500 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> Loaded & Indexed
              </span>
              <button
                onClick={() => onSelectQuery(`tell me about ${ds.filename.replace('.json', '').replace(/_/g, ' ')}`)}
                className="text-xs text-emerald-400 hover:text-emerald-300 flex items-center gap-1 font-medium cursor-pointer"
              >
                <span>Query</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
