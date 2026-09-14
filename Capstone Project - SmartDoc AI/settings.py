import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"


class Settings:
    @property
    def GEMINI_API_KEY(self) -> str:
        load_dotenv(dotenv_path=env_path, override=True)
        return os.getenv("GEMINI_API_KEY", "")

    @property
    def GEMINI_MODEL(self) -> str:
        load_dotenv(dotenv_path=env_path, override=True)
        return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    @property
    def DATABASE_URL(self) -> str:
        load_dotenv(dotenv_path=env_path, override=True)
        return os.getenv("DATABASE_URL", "sqlite:///documents.db")


settings = Settings()
