from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True
    API_KEY: str
    REMOVE_BG_URL: str
    MP4_TO_MP3_URL: str
    YT_DOWNLOAD_URL: str


    class Config:
        env_file = ".env"

settings = Settings()
