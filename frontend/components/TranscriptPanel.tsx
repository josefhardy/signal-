"use client";

import { useState } from "react";

interface TranscriptPanelProps {
  transcript: string;
}

export default function TranscriptPanel({ transcript }: TranscriptPanelProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="rounded-2xl border border-slate-700 bg-slate-800/40">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between px-6 py-4 text-left text-sm font-semibold text-slate-300 hover:text-slate-100"
      >
        <span>Full Transcript</span>
        <svg
          className={`h-4 w-4 text-slate-400 transition-transform ${open ? "rotate-180" : ""}`}
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={2.5}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="m19 9-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <div className="border-t border-slate-700 px-6 py-4">
          <p className="whitespace-pre-wrap font-mono text-xs leading-relaxed text-slate-400">
            {transcript}
          </p>
        </div>
      )}
    </div>
  );
}
