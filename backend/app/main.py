from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import episodes

app = FastAPI(
    title="Signal API",
    description="Podcast SEO/GEO intelligence platform — backend API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(episodes.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
