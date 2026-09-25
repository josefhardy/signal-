# Podcast SEO/GEO Intelligence Platform — Project Context

_Last updated: 2026-09-25_
_Owner: Josef Hardy (josefmhardy@gmail.com)_

This document is the single source of truth for the product decisions made so far. Any AI session (Claude, another Claude Code instance, etc.) or collaborator should read this file first before doing any work on the project — it replaces re-explaining context from scratch.

---

## 1. What this is

A **SaaS web app for podcasters** that turns a raw episode into a full, data-grounded SEO/discoverability package — and tracks over time whether it's actually working.

**One-line pitch:**
> A performance-benchmarked SEO assistant for podcasters — grounded in what's actually working in your niche, not generic AI suggestions.

**The core insight / moat:** anyone can ask an LLM "write me SEO for this." That's not defensible. What's defensible is:
1. **Proprietary performance data** — tracking what actually works (titles, topics, structure) across many shows in a niche, and grounding suggestions in that data via retrieval, not just LLM intuition.
2. **A closed feedback loop** — suggest → publish → measure real outcomes → improve future suggestions for *this specific show*. A one-off prompt can never do this; it requires memory and measurement over time.
3. **Benchmarking against niche peers** — "shows like yours do X" — a network-effect-lite moat that gets more valuable as more users in a niche join, and that a generic LLM session structurally cannot replicate.

Do not let the "generate SEO text" feature become the headline pitch even though it's the most visible output — the pitch is "data-grounded intelligence," not "AI writes your titles."

---

## 2. Target user & niche

- **Niche: podcasts only, for v1.** Explicitly NOT newsletters, blogs, YouTube, or other creative formats yet — deliberately narrow so benchmarking data has enough density within one format to be meaningful, and so the product can be excellent at one thing rather than mediocre at many. Expansion to other formats is a post-traction decision, not a v1 feature.
- **Buyer:** individual podcasters and small podcast teams (not enterprise media companies for v1).
- **Distribution:** self-serve, no sales calls — podcasting communities (r/podcasting, Podcast Movement community), content marketing/SEO guides for podcasters, possible future integration/partnership with podcast hosting platforms (Buzzsprout, Transistor, etc.). Founder (Josef) prefers technical building over sales/relationship-driven growth, so the whole GTM model is designed around self-serve discovery, not outbound.

---

## 3. Product scope

### Core pipeline (per episode)
1. **Transcription** — audio → full text transcript (also independently useful: gives search engines something to index, which most podcasts currently lack).
2. **Content analysis** — extract topics, entities, key quotes/moments, segment structure from the transcript.
3. **Keyword/trend retrieval** — pull current, relevant search trend data / questions people are asking in that topic area, so suggestions are grounded in real search behavior, not just plausible-sounding text.
4. **Grounded generation** — using transcript + trend data + (later) this show's own history + niche benchmarks, generate:
   - Title options
   - Meta description
   - Full show notes (readable summary + timestamps/chapters)
   - Suggested blog-post version of the episode
   - Relevant tags/categories
5. **Benchmarking (grows with data)** — compare this episode's approach/performance against the show's own history and against similar shows in the niche.

### Dashboard (the "SaaS" surface)
- Episode list/history
- Performance metrics over time (open/click data if connected to hosting platform stats, or manual entry)
- What's working for this show specifically
- Niche benchmark comparisons (as data volume allows)

### What the product is NOT
- Not a fully automated "publish on my behalf" pipeline — suggestions are surfaced for the user to review/edit, not auto-published.
- Not multi-format (no newsletters/blogs/video in v1).
- Not GEO-first (see below) — GEO is a planned secondary layer, not part of MVP.

---

## 4. GEO (Generative Engine Optimization) — planned, not in MVP

GEO = optimizing content to be surfaced/cited by AI answer engines (ChatGPT, Perplexity, Google AI Overviews, etc.), as distinct from traditional search-engine SEO.

**Decision:** GEO is a strong strategic fit long-term (podcasts/newsletters need essentially the same underlying work — good transcripts, structured summaries — for both SEO and GEO, so it's not a second pipeline). It also reinforces the "not a generic LLM wrapper" story, since GEO requires understanding retrieval/citation behavior specifically.

**But:** GEO measurement tooling is immature industry-wide (no "Search Console for AI citations" exists yet), so it's more manual/expensive to measure per user. **Explicit decision: build SEO first, validate the core product and pricing, then add GEO as a differentiating layer once the core loop works.** Do not build GEO into the v1 MVP.

---

## 5. Pricing model (early thinking, not finalized)

Decision so far: **avoid feature-gating SEO vs. GEO** (e.g., "pay more for GEO") — this undersells the "one integrated intelligence engine" story and risks charging a premium for a feature (GEO) that isn't mature/polished yet.

Preferred initial approach: **usage-based tiers with everything included** (e.g., priced by number of episodes processed per month), not feature-based tiers. Example shape (not finalized, needs real pricing research):
- Starter: up to ~4 episodes/month, core SEO package included
- Growth: more episodes, deeper benchmarking, more history

Once there's real usage data, introduce a premium tier built around whichever feature actually proves most valuable to users (may or may not end up being GEO).

**Not yet decided:** actual price points. Needs competitor research and early user willingness-to-pay signal.

---

## 6. Validation status

**Not yet done.** No podcasters have been talked to yet. This is a known gap — recommended (not blocking) next step: post in podcasting communities (r/podcasting, etc.) and DM 5–10 small/mid podcasters about their current SEO/discoverability pain points before investing heavily in build time. Founder has chosen to proceed with building first and validate in parallel/after, which is a conscious risk tradeoff, not an oversight.

---

## 7. MVP scope (what to build first)

Smallest useful loop, explicitly scoped down from the full vision above:

1. User uploads a podcast episode (audio file) or connects an RSS feed.
2. System transcribes the audio.
3. System generates: SEO-optimized title options, description, and show notes — grounded in retrieved keyword/trend data (not just a raw LLM prompt).
4. Results saved to a simple dashboard the user can view, edit, and copy from.

Explicitly OUT of MVP scope: GEO features, niche benchmarking (needs multiple users' data to be meaningful anyway), billing/subscription polish, RSS auto-publishing, hosting-platform analytics integrations.

---

## 8. Technical decisions

- **Repo:** https://github.com/josefhardy/signal- (created directly on GitHub by the founder).
- **Stack (recommended, not yet locked in code):**
  - Backend: Python/FastAPI (good fit for AI/ML pipeline work, easy to integrate transcription + LLM APIs)
  - Transcription: managed API (e.g., Whisper via an API provider) rather than self-hosting, to move fast as a solo dev
  - LLM generation: via API (provider not yet fixed)
  - Database: Postgres
  - Frontend: React/Next.js
  - Deployment: not yet decided (Vercel/Railway/AWS — a later decision once there's something to deploy)
- **Second brain / notes:** founder uses Obsidian; this markdown file is designed to be readable/linkable from Obsidian as well as GitHub.

---

## 9. Founder profile (relevant to product/business decisions)

- Solo founder, computer science student, planning to start immediately after graduating.
- Prefers deep technical building over sales/relationship-driven work — this has shaped GTM (self-serve, content/community-led, not outbound sales) and product shape (dev-tool-adjacent distribution patterns even though the buyer is podcasters, not developers).
- No pre-existing industry connections/insight in podcasting specifically — chose this niche via reasoning about market gaps, not personal domain expertise. Worth compensating for with genuine user validation before/alongside building.
- Open to the business growing beyond solo eventually, but structured to be buildable and runnable by one person initially.

---

## 10. Open questions / not yet decided

- Actual pricing figures
- Which transcription/LLM providers specifically
- Whether to integrate with podcast hosting platforms' APIs for real performance data, and which ones first
- Deployment/hosting choice
- Whether/how to do user validation before or during MVP build
- Legal/liability considerations (lower stakes than the legal-contract or medical ideas considered earlier, but still worth a basic ToS/disclaimer once real users are involved)

---

## 11. Ideas considered and explicitly rejected (for context, avoid re-litigating)

- RAG-as-the-business generically (too generic, not defensible alone) — RAG is a technique, not a product.
- Legal contract cross-referencing tool — good business, but higher liability exposure and longer/harder sales cycle for a solo first project.
- Construction/engineering compliance (blueprint + code checking) — strong business but hardest MVP technically (CAD parsing is a hard, semi-unsolved problem).
- Medical multimodal tool (scans + notes + labs) — deprioritized: heavy regulation (HIPAA, possible FDA medical device classification), long hospital sales cycles, highest stakes for mistakes. Parked for much later, if ever.
- Gym/sports vertical ideas — founder is involved in the space but wasn't excited by any of the specific product ideas proposed.
- Multi-format ("as many creative arts as possible") from day one — explicitly rejected in favor of podcasts-only v1, to keep benchmarking data dense and avoid building something mediocre at many things instead of excellent at one.
