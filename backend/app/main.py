from fastapi import FastAPI

from app.routers import episodes

app = FastAPI(
    title="Signal API",
    description="Podcast SEO/GEO intelligence platform — backend API.",
    version="0.1.0",
)

app.include_router(episodes.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
