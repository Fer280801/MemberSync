from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str | None = None
    SECRET_KEY: str | None = None
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    CORS_ALLOWED_ORIGINS: str | None = None
    CORS_ALLOW_ORIGIN_REGEX: str = r"^https://.*\.netlify\.app$"

    class Config:
        env_file = ".env"


settings = Settings()
