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
  - retrieve_trend_data(): implemented via pytrends (Google Trends,
    free/unofficial). Degrades gracefully to [] on rate-limit/network
    error. Upgrade path: swap for SerpApi/DataForSEO when reliability
    or richer data (actual volume, PAA) becomes worth paying for.
  - generate_seo_package(): fully wired — trend data now flows into
    the generation prompt when available.

Not in MVP yet (see PROJECT_CONTEXT.md §7):
  - This show's own historical performance data.
  - Niche benchmark data across similar shows.
"""

import asyncio
import json
import logging
from dataclasses import dataclass

from openai import OpenAI
from pytrends.request import TrendReq

from app.config import settings

logger = logging.getLogger(__name__)

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
    topics: list[str]       # descriptive phrases — used for show notes context
    entities: list[str]
    key_quotes: list[str]
    search_keywords: list[str]  # short query-style terms — fed to retrieve_trend_data()


async def extract_topics(transcript: str) -> TopicExtraction:
    """Pull structured topics/entities/quotes out of a raw transcript.

    Returns two distinct representations of the episode's subject matter:
    - topics: descriptive summary phrases (used in show notes generation)
    - search_keywords: short 2-4 word phrases the way someone would type
      into Google (used for trend lookup — these are what pytrends can
      actually match against real search volume)
    """
    client = _get_client()

    prompt = f"""Analyze this podcast episode transcript and extract:
1. Main topics discussed (3-6 descriptive phrases summarising what was covered)
2. Named entities mentioned (people, companies, products, places)
3. The 2-4 most quotable/interesting moments (verbatim short quotes)
4. Search keywords: 4-6 short phrases (2-4 words each) that someone would
   actually type into Google to find content like this episode. These must
   be concise, search-query style — NOT descriptive summaries. Good examples:
   "green lantern review", "DC show 2024", "hal jordan character". Bad
   examples: "Comparisons with past DC shows", "Character analysis of the
   Green Lanterns in the new series".

Return ONLY valid JSON in this exact shape:
{{"topics": [...], "entities": [...], "key_quotes": [...], "search_keywords": [...]}}

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
        search_keywords=data.get("search_keywords", []),
    )


def _fetch_trends_sync(topics: list[str]) -> list[dict]:
    """
    Synchronous pytrends fetch — runs in a thread via asyncio.to_thread()
    so it doesn't block the event loop.

    pytrends is an unofficial Google Trends client: free, no API key,
    but rate-limited (429s under heavy load) and occasionally flaky.
    We degrade gracefully — any exception returns [] so the rest of the
    pipeline still runs with the "NOT YET AVAILABLE" notice in the prompt.

    Upgrade path: when reliability or richer data (actual search volume,
    People Also Ask) becomes worth paying for, swap the pytrends calls
    here for a SerpApi / DataForSEO call and keep the return shape
    identical. Nothing else in the pipeline needs to change.
    """
    results: list[dict] = []
    pytrends = TrendReq(hl="en-US", tz=0, timeout=(10, 30))

    # pytrends caps keyword batches at 5.
    BATCH = 5
    for i in range(0, len(topics), BATCH):
        batch = topics[i : i + BATCH]
        try:
            pytrends.build_payload(batch, cat=0, timeframe="today 3-m", geo="")

            # Interest over time: 0–100 scale Google uses internally.
            iot = pytrends.interest_over_time()
            # Related queries for each keyword — "rising" entries are the
            # most useful signal ("queries that have increased significantly").
            related = pytrends.related_queries()

            for kw in batch:
                # Average interest over the period as a proxy for "volume".
                interest = 0
                trend_dir = "stable"
                if not iot.empty and kw in iot.columns:
                    series = iot[kw]
                    interest = int(series.mean())
                    # Simple trend direction: compare last third vs first third.
                    n = len(series)
                    if n >= 6:
                        early = series.iloc[: n // 3].mean()
                        late = series.iloc[-n // 3 :].mean()
                        if late > early * 1.2:
                            trend_dir = "rising"
                        elif late < early * 0.8:
                            trend_dir = "falling"

                # Rising related queries are the "what people actually search"
                # signal. Take up to 5 per keyword, deduplicated.
                rising_queries: list[str] = []
                if kw in related and related[kw].get("rising") is not None:
                    df_rising = related[kw]["rising"]
                    if df_rising is not None and not df_rising.empty:
                        rising_queries = df_rising["query"].head(5).tolist()

                results.append(
                    {
                        "keyword": kw,
                        "interest": interest,  # 0–100, Google Trends scale
                        "trend": trend_dir,    # "rising" | "falling" | "stable"
                        "related_questions": rising_queries,
                    }
                )
        except Exception as exc:
            # Rate-limited or network error — log and skip this batch rather
            # than failing the whole pipeline.
            logger.warning("pytrends fetch failed for batch %s: %s", batch, exc)

    return results


async def retrieve_trend_data(topics: list[str]) -> list[dict]:
    """
    Retrieve current search/trend data for the given topics via Google Trends.

    Returns a list of dicts:
        [{"keyword": str, "interest": int, "trend": str, "related_questions": list[str]}]

    "interest" is Google Trends' 0–100 relative-interest score averaged over
    the last 3 months. "trend" is "rising" | "falling" | "stable" based on
    whether interest increased/decreased more than 20% from the first to the
    last third of that window. "related_questions" are rising related queries
    — the closest proxy we have (for free) to "what people are actually
    searching" around this topic.

    Degrades gracefully to [] on any network or rate-limit error so the
    pipeline continues with the "trend data not available" notice in the
    generation prompt.
    """
    if not topics:
        return []
    return await asyncio.to_thread(_fetch_trends_sync, topics)


async def generate_seo_package(transcript: str) -> SeoPackage:
    """
    Generate a grounded SEO package for an episode.

    Runs the full grounding pipeline: extract topics from the
    transcript, retrieve trend data for those topics, then generate
    suggestions with both pieces of context explicit in the prompt.
    """
    client = _get_client()

    extraction = await extract_topics(transcript)
    trend_data = await retrieve_trend_data(extraction.search_keywords)

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
    seo_package = SeoPackage(
        title_options=data.get("title_options", []),
        meta_description=data.get("meta_description", ""),
        show_notes=data.get("show_notes", ""),
        tags=data.get("tags", []),
    )
    return seo_package, trend_data
