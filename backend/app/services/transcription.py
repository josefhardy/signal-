"""
Transcription service.

Uses OpenAI's Whisper API to turn an uploaded audio file into a full
text transcript. Kept behind a small function boundary so the provider
can be swapped later without touching callers.
"""

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
class TranscriptionResult:
    text: str
    # Whisper's verbose_json response includes per-segment timestamps,
    # useful later for show-notes chapter markers. Kept as raw dicts
    # for now rather than a typed model, since we don't consume them yet.
    segments: list[dict]


async def transcribe_audio(file_path: str) -> TranscriptionResult:
    """
    Transcribe an audio file at `file_path` and return the transcript.

    Note: the OpenAI SDK's transcription call is synchronous under the
    hood; for an MVP with low concurrency this is fine. If upload volume
    grows, move this to a background task/queue rather than blocking
    the request.
    """
    client = _get_client()

    with open(file_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model=settings.transcription_model,
            file=audio_file,
            response_format="verbose_json",
        )

    # response.segments is a list of Segment objects when using
    # verbose_json; normalize to plain dicts for easy JSON storage.
    segments = [
        {
            "start": seg.start,
            "end": seg.end,
            "text": seg.text,
        }
        for seg in getattr(response, "segments", []) or []
    ]

    return TranscriptionResult(text=response.text, segments=segments)
