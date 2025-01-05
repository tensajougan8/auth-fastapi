from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE_URL: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    FACEBOOK_CLIENT_ID: str
    FACEBOOK_CLIENT_SECRET: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    GOOGLE_REDIRECT_URL: str

    class Config:
        # This will look for .env file in the auth directory (2 levels up from core)
        env_file = Path(__file__).parent.parent.parent / ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()