"""
Episode upload + SEO package endpoints.

MVP flow (see PROJECT_CONTEXT.md §7):
  POST /episodes/upload      -> accept audio, transcribe, generate SEO package
  GET  /episodes/{id}        -> fetch a single episode's result
  GET  /episodes             -> list all episodes (for the dashboard)

Storage is a simple JSON-file store for now (see services/storage.py);
swap for a real DB once the pipeline itself is proven out.
"""

import os
import uuid
from dataclasses import asdict

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.config import settings
from app.services import storage
from app.services.seo_generation import generate_seo_package
from app.services.transcription import transcribe_audio

router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.post("/upload")
async def upload_episode(file: UploadFile = File(...)):
    """
    Accept an uploaded audio file, transcribe it, generate a grounded
    SEO package, and persist the result.

    Synchronous/blocking for the MVP — transcription + generation for
    a typical episode takes well under a minute, which is acceptable
    for a first version. If this becomes a bottleneck (long episodes,
    concurrent uploads), move to a background task queue.
    """
    episode_id = str(uuid.uuid4())

    os.makedirs(settings.uploads_dir, exist_ok=True)
    file_extension = os.path.splitext(file.filename or "")[1] or ".mp3"
    saved_path = os.path.join(settings.uploads_dir, f"{episode_id}{file_extension}")

    with open(saved_path, "wb") as f:
        f.write(await file.read())

    try:
        transcription = await transcribe_audio(saved_path)
        seo_package = await generate_seo_package(transcription.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {e}")

    result = {
        "id": episode_id,
        "original_filename": file.filename,
        "transcript": transcription.text,
        "segments": transcription.segments,
        "seo_package": asdict(seo_package),
    }
    storage.save_episode(episode_id, result)

    return result


@router.get("")
async def list_episodes():
    """List all episodes, most recent first, for the dashboard."""
    episodes = storage.list_episodes()
    return sorted(episodes, key=lambda e: e.get("created_at", ""), reverse=True)


@router.get("/{episode_id}")
async def get_episode(episode_id: str):
    """Fetch a single episode and its generated SEO package."""
    episode = storage.load_episode(episode_id)
    if episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode
