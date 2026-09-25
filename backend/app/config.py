from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    database_url: str = "postgresql://user:password@localhost:5432/signal"
    transcription_api_key: str = ""
    llm_api_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
