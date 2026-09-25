"use client";

import { useState } from "react";

interface TagPillProps {
  tag: string;
}

export default function TagPill({ tag }: TagPillProps) {
  const [copied, setCopied] = useState(false);

  const handleClick = async () => {
    try {
      await navigator.clipboard.writeText(tag);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // ignore
    }
  };

  return (
    <button
      onClick={handleClick}
      title={`Copy "${tag}"`}
      className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
        copied
          ? "bg-emerald-800/50 text-emerald-300 ring-1 ring-emerald-500/40"
          : "bg-slate-700 text-slate-300 hover:bg-indigo-800/60 hover:text-indigo-200"
      }`}
    >
      {copied ? "Copied!" : tag}
    </button>
  );
}
