import Link from "next/link";
import { notFound } from "next/navigation";
import { getEpisode } from "@/lib/api";
import CopyButton from "@/components/CopyButton";
import TranscriptPanel from "@/components/TranscriptPanel";
import TagPill from "@/components/TagPill";

interface Props {
  params: Promise<{ id: string }>;
}

export default async function EpisodePage({ params }: Props) {
  const { id } = await params;

  let episode;
  try {
    episode = await getEpisode(id);
  } catch {
    notFound();
  }

  const { seo_package, transcript, original_filename, created_at } = episode;

  return (
    <main className="mx-auto w-full max-w-2xl px-4 py-12">
      {/* Back nav */}
      <Link
        href="/"
        className="mb-8 inline-flex items-center gap-1.5 text-sm text-slate-400 transition-colors hover:text-slate-200"
      >
        <svg
          className="h-4 w-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth={2.5}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M15.75 19.5 8.25 12l7.5-7.5"
          />
        </svg>
        Dashboard
      </Link>

      {/* Episode header */}
      <header className="mb-8">
        <h1 className="break-words text-2xl font-bold text-white">
          {seo_package.title_options[0] ?? original_filename ?? id}
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          {original_filename}
          {created_at && (
            <> &middot; {new Date(created_at).toLocaleDateString("en-US", {
              year: "numeric",
              month: "long",
              day: "numeric",
            })}</>
          )}
        </p>

        {/* Grounding badge */}
        <div className="mt-3 inline-flex items-center gap-1.5 rounded-full border border-indigo-500/30 bg-indigo-900/20 px-3 py-1 text-xs font-medium text-indigo-300">
          <svg
            className="h-3.5 w-3.5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 0 1 3 19.875v-6.75ZM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V8.625ZM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 0 1-1.125-1.125V4.125Z"
            />
          </svg>
          Generated with Google Trends grounding
        </div>
      </header>

      <div className="flex flex-col gap-6">
        {/* Title options */}
        <section className="rounded-2xl border border-slate-700 bg-slate-800/40 p-6">
          <h2 className="mb-4 text-xs font-semibold uppercase tracking-widest text-slate-500">
            Title Options
          </h2>
          <ul className="flex flex-col gap-3">
            {seo_package.title_options.map((title, i) => (
              <li
                key={i}
                className="flex items-start justify-between gap-3 rounded-xl bg-slate-900/50 px-4 py-3"
              >
                <span className="flex-1 text-sm text-slate-200">{title}</span>
                <CopyButton text={title} />
              </li>
            ))}
          </ul>
        </section>

        {/* Meta description */}
        <section className="rounded-2xl border border-slate-700 bg-slate-800/40 p-6">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-500">
              Meta Description
            </h2>
            <CopyButton text={seo_package.meta_description} />
          </div>
          <p className="text-sm leading-relaxed text-slate-300">
            {seo_package.meta_description}
          </p>
        </section>

        {/* Show notes */}
        <section className="rounded-2xl border border-slate-700 bg-slate-800/40 p-6">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-500">
              Show Notes
            </h2>
            <CopyButton text={seo_package.show_notes} />
          </div>
          <p className="whitespace-pre-wrap text-sm leading-relaxed text-slate-300">
            {seo_package.show_notes}
          </p>
        </section>

        {/* Tags */}
        <section className="rounded-2xl border border-slate-700 bg-slate-800/40 p-6">
          <h2 className="mb-4 text-xs font-semibold uppercase tracking-widest text-slate-500">
            Tags
          </h2>
          <div className="flex flex-wrap gap-2">
            {seo_package.tags.map((tag, i) => (
              <TagPill key={i} tag={tag} />
            ))}
          </div>
        </section>

        {/* Full transcript (collapsible) */}
        <TranscriptPanel transcript={transcript} />
      </div>
    </main>
  );
}
