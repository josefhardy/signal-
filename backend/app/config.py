from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    database_url: str = "postgresql://user:password@localhost:5432/signal"

    # Using OpenAI for both transcription (Whisper) and generation (chat
    # completions) to start — one key, two capabilities. Swap out later
    # if a different provider makes sense for either piece.
    openai_api_key: str = ""

    # Model choices, kept configurable rather than hardcoded inline.
    transcription_model: str = "whisper-1"
    generation_model: str = "gpt-4o-mini"

    # Where uploaded audio / generated results live for the MVP.
    # No real database yet (see PROJECT_CONTEXT.md §10) — this is a
    # deliberately simple JSON-file store so the pipeline is testable
    # end-to-end before we invest in Postgres/SQLAlchemy.
    data_dir: str = "data"
    uploads_dir: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
