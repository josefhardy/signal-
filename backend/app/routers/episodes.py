"""
Episode upload + SEO package endpoints.

MVP flow (see PROJECT_CONTEXT.md section 7):
  POST /episodes/upload  -> accept audio file, kick off transcription
  GET  /episodes/{id}    -> fetch episode + its generated SEO package

Storage/DB wiring is not implemented yet — this is the routing skeleton
so the pipeline shape is clear before we lock in the database layer.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/episodes", tags=["episodes"])


@router.post("/upload")
async def upload_episode(file: UploadFile = File(...)):
    """
    Accept an uploaded audio file, save it, and (eventually) trigger
    the transcription -> SEO generation pipeline.
    """
    raise HTTPException(
        status_code=501,
        detail=(
            "Not implemented yet. Next steps: save the uploaded file, "
            "call app.services.transcription.transcribe_audio, then "
            "app.services.seo_generation.generate_seo_package, and "
            "persist the result."
        ),
    )


@router.get("/{episode_id}")
async def get_episode(episode_id: str):
    """Fetch a single episode and its generated SEO package."""
    raise HTTPException(status_code=501, detail="Not implemented yet — needs DB layer.")
