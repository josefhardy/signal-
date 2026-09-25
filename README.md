# Signal

A performance-benchmarked SEO/GEO assistant for podcasters — grounded in what's actually working in your niche, not generic AI suggestions.

**Start here:** [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) has the full product spec, decisions made so far, and open questions. Read it before making product or architecture changes.

## Status

Early scaffold. Backend skeleton exists (FastAPI); core pipeline logic (transcription, grounded SEO generation) is stubbed with `NotImplementedError` and TODOs pointing at what to build next. No frontend yet.

## Structure

```
signal/
├── PROJECT_CONTEXT.md     # full product spec — read this first
├── backend/                # FastAPI app
│   └── app/
│       ├── main.py
│       ├── config.py
│       ├── routers/
│       │   └── episodes.py       # upload + fetch endpoints (stubbed)
│       └── services/
│           ├── transcription.py   # audio -> transcript (stubbed)
│           └── seo_generation.py  # transcript + trend data -> SEO package (stubbed)
└── frontend/                # not yet scaffolded — see below
```

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in real API keys once providers are chosen
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/health` to confirm it's running, and `http://localhost:8000/docs` for the interactive API docs.

## Frontend

Not scaffolded yet. When ready:

```bash
npx create-next-app@latest frontend --typescript --tailwind --app
```

## Next steps (see PROJECT_CONTEXT.md §7 and §10)

1. Pick a transcription provider and wire up `services/transcription.py`.
2. Pick a keyword/trend data source and an LLM provider, wire up `services/seo_generation.py` — **make sure generation is grounded in retrieved trend data, not just the raw transcript** (this is the whole point of the product's moat, see `PROJECT_CONTEXT.md` §1).
3. Add a database layer (Postgres + SQLAlchemy) and persist episodes/SEO packages.
4. Scaffold the frontend and build the upload -> dashboard flow.
5. Validate with real podcasters (not yet done — see `PROJECT_CONTEXT.md` §6).
