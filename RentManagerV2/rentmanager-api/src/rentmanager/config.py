from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	app_name: str = "RentManager API"
	app_env: str = "dev"
	app_debug: bool = True
	app_secret_key: str = "change-me-in-real-environments-32b"
	jwt_algorithm: str = "RS256"
	jwt_private_key_path: str = ".keys/private_key.pem"
	jwt_public_key_path: str = ".keys/public_key.pem"
	access_token_expire_minutes: int = 15
	refresh_token_expire_days: int = 7
	database_url: str = "mysql+pymysql://rentmanager:rentmanager@localhost:3306/rentmanager"

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)


@lru_cache
def get_settings() -> Settings:
	return Settings()


def resolve_project_path(relative_path: str) -> Path:
	"""Resolve paths from project root regardless of current working directory."""

	base_dir = Path(__file__).resolve().parents[2]
	return base_dir / relative_path

