"""
Transcription service.

MVP plan: send the uploaded audio file to a managed transcription API
(e.g. OpenAI's Whisper API) and return the full text transcript, plus
timestamped segments if the provider supports them (useful later for
show-notes chapter markers).

Deliberately provider-agnostic at the function boundary so we can swap
providers without touching callers.
"""

from app.config import settings


class TranscriptionResult:
    def __init__(self, text: str, segments: list[dict] | None = None):
        self.text = text
        self.segments = segments or []


async def transcribe_audio(file_path: str) -> TranscriptionResult:
    """
    Transcribe an audio file and return the transcript.

    TODO: implement actual API call once a provider is chosen
    (see PROJECT_CONTEXT.md section 8/10 — not yet decided).
    """
    raise NotImplementedError(
        "Wire this up to a transcription provider (e.g. OpenAI Whisper API) "
        "using settings.transcription_api_key."
    )
