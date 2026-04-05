from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_BACKEND_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _BACKEND_DIR.parent


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_user: str
    db_password: str
    db_name: str = "eqwatch"

    model_config = SettingsConfigDict(
        env_file=(
            _REPO_ROOT / ".env",
            _BACKEND_DIR / ".env",
        ),
        env_file_encoding="utf-8",
    )


settings = Settings()
