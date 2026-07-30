import os
from pathlib import Path
from typing import Literal

import os

ROOT = Path(__file__).resolve().parent.parent

class Settings:
    """Application settings loaded from environment variables."""

    ENV: Literal["development", "production"]
    SITE_TITLE: str
    ANALYTICS_ID: str | None
    DATABASE_URL: str
    DATABASE_MAX_CONNECTIONS: int

    def __init__(self) -> None:
        self.ENV = os.getenv("PROFILE_SITE_ENV", "development")
        if self.ENV not in ("development", "production"):
            raise ValueError("PROFILE_SITE_ENV must be 'development' or 'production'.")

        self.SITE_TITLE = os.getenv("SITE_TITLE", "Mckinzy | Professional Bio")
        self.ANALYTICS_ID = os.getenv("ANALYTICS_ID")
        self.DATABASE_URL = os.getenv("DATABASE_URL", str(ROOT / "data" / "profile_site.db"))

        try:
            self.DATABASE_MAX_CONNECTIONS = int(os.getenv("DATABASE_MAX_CONNECTIONS", "5"))
        except ValueError as exc:
            raise ValueError("DATABASE_MAX_CONNECTIONS must be an integer.") from exc

    @classmethod
    def from_env(cls) -> "Settings":
        return cls()


settings = Settings.from_env()
