"use client";

import { useState, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import { uploadEpisode } from "@/lib/api";

const ACCEPTED_TYPES = [".mp3", ".mp4", ".wav", ".m4a"];
const ACCEPTED_MIME = [
  "audio/mpeg",
  "audio/mp4",
  "audio/wav",
  "audio/x-wav",
  "audio/x-m4a",
  "audio/m4a",
  "video/mp4",
];

export default function UploadZone() {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFile = useCallback(
    async (file: File) => {
      setError(null);
      setLoading(true);
      try {
        const episode = await uploadEpisode(file);
        router.push(`/episodes/${episode.id}`);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Upload failed");
        setLoading(false);
      }
    },
    [router]
  );

  const onDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault();
      setIsDragging(false);
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [handleFile]
  );

  const onDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const onDragLeave = () => setIsDragging(false);

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 rounded-2xl border border-indigo-500/40 bg-slate-800/60 p-12 text-center">
        <svg
          className="h-10 w-10 animate-spin text-indigo-400"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
          />
        </svg>
        <p className="text-lg font-medium text-slate-200">
          Transcribing &amp; generating SEO package&hellip;
        </p>
        <p className="text-sm text-slate-400">This can take 30–60 seconds.</p>
      </div>
    );
  }

  return (
    <div>
      <div
        role="button"
        tabIndex={0}
        onClick={() => inputRef.current?.click()}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
        onDrop={onDrop}
        onDragOver={onDragOver}
        onDragLeave={onDragLeave}
        className={`flex cursor-pointer flex-col items-center justify-center gap-3 rounded-2xl border-2 border-dashed p-12 text-center transition-colors ${
          isDragging
            ? "border-indigo-400 bg-indigo-900/30"
            : "border-slate-600 bg-slate-800/40 hover:border-indigo-500/60 hover:bg-slate-800/60"
        }`}
      >
        <svg
          className="h-12 w-12 text-slate-400"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={1.5}
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 16.5V9.75m0 0 3 3m-3-3-3 3M6.75 19.5a4.5 4.5 0 0 1-1.41-8.775 5.25 5.25 0 0 1 10.338-2.32 5.75 5.75 0 0 1 1.83 11.095H6.75Z"
          />
        </svg>
        <div>
          <p className="text-base font-semibold text-slate-200">
            Drop an audio file here, or{" "}
            <span className="text-indigo-400 underline underline-offset-2">
              browse
            </span>
          </p>
          <p className="mt-1 text-sm text-slate-400">
            {ACCEPTED_TYPES.join(", ")} supported
          </p>
        </div>
      </div>

      <input
        ref={inputRef}
        type="file"
        accept={[...ACCEPTED_TYPES, ...ACCEPTED_MIME].join(",")}
        className="hidden"
        onChange={onInputChange}
      />

      {error && (
        <p className="mt-3 rounded-lg bg-red-900/30 px-4 py-2 text-sm text-red-300">
          {error}
        </p>
      )}
    </div>
  );
}
