from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    DEBUG: bool = True

settings = Settings()
