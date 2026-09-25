"""
SEO generation service — the core "grounded generation" step.

Important (see PROJECT_CONTEXT.md section 1): this must NOT be a bare
LLM prompt ("write SEO for this transcript"). The whole point of the
product's moat is that suggestions are grounded in retrieved data, not
just the transcript + model intuition.

MVP grounding sources (see PROJECT_CONTEXT.md section 7 for MVP scope):
  1. The episode transcript itself (topics, entities, key quotes).
  2. Current keyword/search-trend data for the episode's topic area.

Not in MVP yet, add later:
  3. This show's own historical performance data.
  4. Niche benchmark data across similar shows.

Each of these should be retrieved and passed into the generation prompt
as explicit context, so the output is traceable back to real data rather
than being a plausible-sounding guess.
"""

from dataclasses import dataclass


@dataclass
class SeoPackage:
    title_options: list[str]
    meta_description: str
    show_notes: str
    tags: list[str]


async def generate_seo_package(transcript: str) -> SeoPackage:
    """
    Generate a grounded SEO package for an episode.

    TODO:
      1. Extract topics/entities/key quotes from `transcript`.
      2. Retrieve current keyword/trend data for those topics
         (search trend API — provider not yet chosen).
      3. Build a generation prompt that explicitly includes the
         retrieved trend data as grounding context, not just the
         transcript.
      4. Call the LLM provider (settings.llm_api_key) and parse the
         result into a SeoPackage.
    """
    raise NotImplementedError(
        "Implement topic extraction, trend retrieval, and grounded "
        "generation. Do not skip straight to an LLM call on the raw "
        "transcript alone — that defeats the product's moat."
    )
