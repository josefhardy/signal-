const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface Segment {
  start: number;
  end: number;
  text: string;
}

export interface SeoPackage {
  title_options: string[];
  meta_description: string;
  show_notes: string;
  tags: string[];
}

export interface Episode {
  id: string;
  original_filename: string;
  created_at?: string;
  transcript: string;
  segments: Segment[];
  seo_package: SeoPackage;
}

export async function listEpisodes(): Promise<Episode[]> {
  const res = await fetch(`${API_URL}/episodes`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch episodes: ${res.status}`);
  }
  return res.json();
}

export async function getEpisode(id: string): Promise<Episode> {
  const res = await fetch(`${API_URL}/episodes/${id}`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Failed to fetch episode ${id}: ${res.status}`);
  }
  return res.json();
}

export async function uploadEpisode(file: File): Promise<Episode> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/episodes/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Upload failed (${res.status}): ${detail}`);
  }
  return res.json();
}
