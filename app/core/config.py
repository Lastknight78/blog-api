from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    API_V1_STR: str = "/api/v1"

    CORS_ORIGINS: List[AnyHttpUrl] = []

    STORAGE_TYPE: str = "file"
    BASE_FILE_URL: str = "/uploads"
    BASE_FILE_PATH: str = "uploads"

    USE_SQLITE: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
