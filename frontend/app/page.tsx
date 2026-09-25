import { Suspense } from "react";
import UploadZone from "@/components/UploadZone";
import EpisodeList from "@/components/EpisodeList";

export default function DashboardPage() {
  return (
    <main className="mx-auto w-full max-w-2xl px-4 py-12">
      {/* Header */}
      <header className="mb-10">
        <h1 className="text-4xl font-bold tracking-tight text-white">
          Signal
          <span className="text-indigo-400">-</span>
        </h1>
        <p className="mt-2 text-base text-slate-400">
          Data-grounded SEO for podcasters
        </p>
      </header>

      {/* Upload section */}
      <section className="mb-10">
        <h2 className="mb-3 text-xs font-semibold uppercase tracking-widest text-slate-500">
          New Episode
        </h2>
        <UploadZone />
      </section>

      {/* Episode list */}
      <section>
        <h2 className="mb-4 text-xs font-semibold uppercase tracking-widest text-slate-500">
          Episodes
        </h2>
        <Suspense
          fallback={
            <p className="text-sm text-slate-500">Loading episodes&hellip;</p>
          }
        >
          <EpisodeList />
        </Suspense>
      </section>
    </main>
  );
}
