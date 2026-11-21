from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Read configuration once per app instance; environment overrides .env."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        env_prefix="MEDILUX_",
        extra="ignore",
    )

    app_name: str = Field(default="MEDILUX API", min_length=1)
    environment: Literal["development", "test", "production"] = "development"
    docs_enabled: bool = True
    cors_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    @field_validator("cors_origins")
    @classmethod
    def validate_origins(cls, origins: list[str]) -> list[str]:
        normalized = []
        for origin in origins:
            parsed = urlsplit(origin)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
                or parsed.path not in {"", "/"}
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError(
                    "CORS origins must be HTTP(S) origins without paths or credentials"
                )
            # Accessing port also validates malformed and out-of-range ports.
            _ = parsed.port
            normalized.append(origin.rstrip("/"))
        return list(dict.fromkeys(normalized))
