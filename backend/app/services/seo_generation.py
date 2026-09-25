"""
SEO generation service — the core "grounded generation" step.

Important (see PROJECT_CONTEXT.md §1): this must NOT be a bare LLM
prompt ("write SEO for this transcript"). The product's whole moat is
that suggestions are grounded in retrieved data, not just the
transcript + model intuition. This module is structured to make that
grounding step explicit and hard to accidentally skip:

    transcript -> extract_topics() -> retrieve_trend_data() -> generate_seo_package()

Current state (v0, see PROJECT_CONTEXT.md §7 for MVP scope):
  - extract_topics(): implemented, uses the LLM to pull structured
    topics/entities/quotes out of the transcript.
  - retrieve_trend_data(): STUBBED. Returns an empty list for now.
    This is the most important piece to replace before this product
    is actually defensible — see the TODO below for concrete options.
  - generate_seo_package(): implemented, but the "grounding" context
    it passes to the LLM is currently topics-only until trend data
    is wired up. Once retrieve_trend_data() does something real, no
    other code needs to change — it's already threaded through.

Not in MVP yet (see PROJECT_CONTEXT.md §7):
  - This show's own historical performance data.
  - Niche benchmark data across similar shows.
"""

import json
from dataclasses import dataclass

from openai import OpenAI

from app.config import settings

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


@dataclass
class SeoPackage:
    title_options: list[str]
    meta_description: str
    show_notes: str
    tags: list[str]


@dataclass
class TopicExtraction:
    topics: list[str]
    entities: list[str]
    key_quotes: list[str]


async def extract_topics(transcript: str) -> TopicExtraction:
    """Pull structured topics/entities/quotes out of a raw transcript."""
    client = _get_client()

    prompt = f"""Analyze this podcast episode transcript and extract:
1. Main topics discussed (3-6 short phrases)
2. Named entities mentioned (people, companies, products, places)
3. The 2-4 most quotable/interesting moments (verbatim short quotes)

Return ONLY valid JSON in this exact shape:
{{"topics": [...], "entities": [...], "key_quotes": [...]}}

Transcript:
{transcript[:12000]}
"""  # truncate to keep prompt size sane for very long episodes

    response = client.chat.completions.create(
        model=settings.generation_model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)
    return TopicExtraction(
        topics=data.get("topics", []),
        entities=data.get("entities", []),
        key_quotes=data.get("key_quotes", []),
    )


async def retrieve_trend_data(topics: list[str]) -> list[dict]:
    """
    Retrieve current search/trend data for the given topics.

    STUB — returns [] for now. This is the grounding step that makes
    generated suggestions defensible ("what people are actually
    searching") rather than just LLM guesswork, so it should be
    prioritized before this product is shown to real users.

    Concrete options to implement this, roughly cheapest/fastest to
    most robust:
      1. Google Trends via an unofficial client (e.g. `pytrends`) —
         free, no API key, but rate-limited and occasionally flaky.
      2. A paid SERP/keyword API (SerpApi, DataForSEO, Ahrefs/SEMrush
         APIs) — more reliable and richer data (search volume,
         related questions), but costs money per query.
      3. A lightweight "People Also Ask" / autocomplete scrape for the
         topic — cheap signal, less robust than a real keyword API.

    Whichever is chosen, keep the return shape as a list of dicts, e.g.
    [{"keyword": "...", "volume": 1200, "trend": "rising"}], so
    generate_seo_package() doesn't need to change.
    """
    return []


async def generate_seo_package(transcript: str) -> SeoPackage:
    """
    Generate a grounded SEO package for an episode.

    Runs the full grounding pipeline: extract topics from the
    transcript, retrieve trend data for those topics, then generate
    suggestions with both pieces of context explicit in the prompt.
    """
    client = _get_client()

    extraction = await extract_topics(transcript)
    trend_data = await retrieve_trend_data(extraction.topics)

    grounding_context = f"""Topics discussed: {", ".join(extraction.topics)}
Entities mentioned: {", ".join(extraction.entities)}
Notable quotes: {" | ".join(extraction.key_quotes)}
Current search trend data for these topics: {json.dumps(trend_data) if trend_data else "NOT YET AVAILABLE — trend retrieval is not implemented yet, see seo_generation.py TODO. Suggestions below are based on transcript content only, not verified search behavior."}
"""

    prompt = f"""You are an SEO assistant for podcasters. Using the grounding
context below, generate an SEO package for this episode.

{grounding_context}

Full transcript (for reference):
{transcript[:8000]}

Return ONLY valid JSON in this exact shape:
{{
  "title_options": ["...", "...", "..."],
  "meta_description": "...",
  "show_notes": "...",
  "tags": ["...", "..."]
}}

title_options: 3-5 SEO-friendly episode titles.
meta_description: 1-2 sentences, under 160 characters, for search results.
show_notes: a readable summary of the episode a listener would scan before pressing play, written in a few short paragraphs.
tags: 5-8 relevant tags/categories.
"""

    response = client.chat.completions.create(
        model=settings.generation_model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)
    return SeoPackage(
        title_options=data.get("title_options", []),
        meta_description=data.get("meta_description", ""),
        show_notes=data.get("show_notes", ""),
        tags=data.get("tags", []),
    )
