from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	app_name: str = "RentManager API"
	app_env: str = "dev"
	app_debug: bool = True
	app_secret_key: str = "change-me-in-real-environments-32b"
	access_token_expire_minutes: int = 30
	database_url: str = "mysql+pymysql://rentmanager:rentmanager@localhost:3306/rentmanager"

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
		extra="ignore",
	)


@lru_cache
def get_settings() -> Settings:
	return Settings()

