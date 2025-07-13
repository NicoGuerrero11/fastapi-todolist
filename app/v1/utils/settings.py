from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SYNC_DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    REDIS_HOST : str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379"

    model_config = SettingsConfigDict(
        env_file='.env',
        extra="ignore"
    )

Config = Settings()