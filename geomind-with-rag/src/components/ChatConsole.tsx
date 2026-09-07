import React, { useState, useRef, useEffect } from "react";
import { Send, Sparkles, Compass, History, BookOpen, MapPin, CheckCircle, Search, ExternalLink } from "lucide-react";
import { ChatMessage } from "../types";

interface ChatConsoleProps {
  messages: ChatMessage[];
  onSendMessage: (text: string) => void;
  isLoading: boolean;
}

const SAMPLE_QUERIES = [
  { label: "Capital of Kenya", query: "what is the capital of Kenya", icon: MapPin },
  { label: "Everest to Fuji Distance", query: "distance between mount everest and mount fuji", icon: MapPin },
  { label: "World War I Causes", query: "what caused world war 1?", icon: History },
  { label: "Renaissance Era", query: "tell me about the Renaissance", icon: History },
  { label: "Amazon River Profile", query: "tell me about the amazon river", icon: Compass },
  { label: "Separation of Powers", query: "what is separation of powers?", icon: BookOpen },
  { label: "United Nations Mission", query: "tell me about the United Nations", icon: BookOpen },
  { label: "Sahara Desert", query: "what is the sahara desert?", icon: Compass },
];

/** Renders a source as a clickable link if it looks like a URL, plain text otherwise. */
const SourceChip: React.FC<{ source: string }> = ({ source }) => {
  const isUrl = /^https?:\/\//i.test(source);
  if (!isUrl) {
    return <span className="text-slate-400">{source}</span>;
  }
  let hostname = source;
  try {
    hostname = new URL(source).hostname.replace(/^www\./, "");
  } catch {
    // keep raw source string if URL parsing fails
  }
  return (
    <a
      href={source}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1 text-cyan-400 hover:text-cyan-300 underline decoration-cyan-500/30 underline-offset-2"
    >
      {hostname}
      <ExternalLink className="w-3 h-3" />
    </a>
  );
};

export const ChatConsole: React.FC<ChatConsoleProps> = ({ messages, onSendMessage, isLoading }) => {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    onSendMessage(input.trim());
    setInput("");
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] max-w-5xl mx-auto w-full">
      {/* Sample Query Pills */}
      <div className="py-3 px-4 flex items-center gap-2 overflow-x-auto no-scrollbar border-b border-slate-800/80 bg-slate-900/40">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 whitespace-nowrap flex items-center gap-1">
          <Sparkles className="w-3.5 h-3.5 text-emerald-400" /> Prompts:
        </span>
        {SAMPLE_QUERIES.map((sample, idx) => {
          const Icon = sample.icon;
          return (
            <button
              key={idx}
              id={`sample-query-${idx}`}
              onClick={() => onSendMessage(sample.query)}
              disabled={isLoading}
              className="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-800/80 hover:bg-emerald-500/10 hover:text-emerald-300 text-slate-300 border border-slate-700/60 hover:border-emerald-500/30 whitespace-nowrap transition-all cursor-pointer disabled:opacity-50"
            >
              <Icon className="w-3 h-3 text-slate-400" />
              <span>{sample.label}</span>
            </button>
          );
        })}
      </div>

      {/* Message Stream */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {messages.map((msg) => {
          const hasWebSources = !!msg.sources?.some((s) => /^https?:\/\//i.test(s));
          return (
            <div
              key={msg.id}
              className={`flex flex-col fade-in ${msg.role === "user" ? "items-end" : "items-start"}`}
            >
              <div className="flex items-center gap-2 mb-1.5 px-1">
                <span className="text-xs font-semibold text-slate-400">
                  {msg.role === "user" ? "You" : "GeoMind-1"}
                </span>
                <span className="text-[10px] text-slate-500">{msg.timestamp}</span>
              </div>

              <div className={`max-w-3xl ${msg.role === "user" ? "message-user" : "message-assistant"}`}>
                <div className="text-sm leading-relaxed whitespace-pre-wrap font-sans">
                  {msg.content}
                </div>

                {/* GeoMind Metadata Tags */}
                {msg.role === "assistant" && (
                  <div className="mt-4 pt-3 border-t border-slate-700/60 flex flex-wrap items-center gap-2">
                    {hasWebSources && (
                      <span className="badge-info">
                        <Search className="w-3 h-3" /> Live Web Search
                      </span>
                    )}
                    {msg.domain && (
                      <span className="badge-success">
                        Domain: {msg.domain}
                      </span>
                    )}
                    {msg.intent && (
                      <span className="badge-info">
                        Intent: {msg.intent}
                      </span>
                    )}
                    {msg.sources && msg.sources.length > 0 && (
                      <span className="text-[11px] text-slate-400 flex flex-wrap items-center gap-x-2 gap-y-1 ml-auto">
                        <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        {msg.sources.map((s, i) => (
                          <React.Fragment key={i}>
                            {i > 0 && <span className="text-slate-600">•</span>}
                            <SourceChip source={s} />
                          </React.Fragment>
                        ))}
                      </span>
                    )}
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {isLoading && (
          <div className="flex flex-col items-start fade-in">
            <div className="flex items-center gap-2 mb-1.5 px-1">
              <span className="text-xs font-semibold text-slate-400">GeoMind-1</span>
              <span className="text-[10px] text-emerald-400 animate-pulse">Running Neural Forward Pass...</span>
            </div>
            <div className="rounded-2xl rounded-tl-none p-4 bg-slate-800/80 border border-slate-700 flex items-center gap-3">
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-bounce" />
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.2s]" />
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.4s]" />
              <span className="text-xs text-slate-400 font-mono">Synthesizing spatial & historical reasoning...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Box */}
      <div className="p-4 bg-slate-900 border-t border-slate-800">
        <form onSubmit={handleSubmit} className="relative flex items-center">
          <input
            id="chat-input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask GeoMind about geography, mountains, distance, world wars, historical eras, economics..."
            className="form-input pr-12 shadow-inner"
            disabled={isLoading}
          />
          <button
            id="send-button"
            type="submit"
            disabled={isLoading || !input.trim()}
            className="absolute right-2 px-3 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold rounded-lg text-sm transition-all disabled:opacity-40 disabled:hover:bg-emerald-500 flex items-center justify-center cursor-pointer"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
};
