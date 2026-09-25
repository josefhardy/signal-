import Link from "next/link";
import { listEpisodes } from "@/lib/api";

function formatDate(iso?: string) {
  if (!iso) return null;
  try {
    return new Date(iso).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  } catch {
    return null;
  }
}

export default async function EpisodeList() {
  let episodes;
  try {
    episodes = await listEpisodes();
  } catch {
    return (
      <p className="text-sm text-red-400">
        Could not load episodes — is the backend running?
      </p>
    );
  }

  if (episodes.length === 0) {
    return (
      <p className="text-sm text-slate-500">
        No episodes yet. Upload your first episode above.
      </p>
    );
  }

  return (
    <ul className="flex flex-col gap-3">
      {episodes.map((ep) => (
        <li key={ep.id}>
          <div className="flex items-center justify-between rounded-xl border border-slate-700 bg-slate-800/40 px-5 py-4 transition-colors hover:border-slate-600 hover:bg-slate-800/60">
            <div className="min-w-0">
              <p className="truncate text-sm font-medium text-slate-200">
                {ep.original_filename ?? ep.id}
              </p>
              {formatDate(ep.created_at) && (
                <p className="mt-0.5 text-xs text-slate-500">
                  {formatDate(ep.created_at)}
                </p>
              )}
            </div>
            <Link
              href={`/episodes/${ep.id}`}
              className="ml-4 shrink-0 rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white transition-colors hover:bg-indigo-500"
            >
              View
            </Link>
          </div>
        </li>
      ))}
    </ul>
  );
}
