from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    """
    Validates environment configurations using Pydantic Settings.
    """
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    OPENROUTER_API_KEY: str = ""
    ALLOWED_ORIGINS: str = "http://localhost:3000"
    FAISS_INDEX_PATH: str = "./faiss_index"
    EVAL_LOG_PATH: str = "./logs/ragas_eval.jsonl"
    LOG_LEVEL: str = "INFO"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

settings = Settings()
