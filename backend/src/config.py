import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BACKEND_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(os.getenv("ENV_FILE", BACKEND_ENV_FILE))


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required. Set it in backend/.env or the environment.")
    return value


def _optional(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _int(name: str, default: int) -> int:
    raw = _optional(name, str(default))
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer.") from exc


def _bool(name: str, default: bool = False) -> bool:
    raw = _optional(name, str(default)).lower()
    return raw in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret: str
    access_token_expire_minutes: int
    environment: str
    database_echo: bool
    redis_url: str
    slack_webhook_url: str
    sendgrid_api_key: str
    sendgrid_from_email: str
    sla_critical_minutes: int
    sla_high_minutes: int


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=_required("DATABASE_URL"),
        jwt_secret=_required("JWT_SECRET"),
        access_token_expire_minutes=_int("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24),
        environment=_optional("ENVIRONMENT", "development"),
        database_echo=_bool("DATABASE_ECHO", False),
        redis_url=_optional("REDIS_URL", "redis://localhost:6379/0"),
        slack_webhook_url=_optional("SLACK_WEBHOOK_URL"),
        sendgrid_api_key=_optional("SENDGRID_API_KEY"),
        sendgrid_from_email=_optional("SENDGRID_FROM_EMAIL", "alerts@yourapp.com"),
        sla_critical_minutes=_int("SLA_CRITICAL_MINUTES", 15),
        sla_high_minutes=_int("SLA_HIGH_MINUTES", 60),
    )
