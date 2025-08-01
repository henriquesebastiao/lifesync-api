from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str
    SECRET_KEY: str
    VERSION: str = 'dev'
    APP_URL: str = 'http://localhost:8000'


@lru_cache
def get_settings():
    return Settings()
