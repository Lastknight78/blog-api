from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from pydantic import field_validator, PostgresDsn, ValidationInfo


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    API_V1_STR: str = "/api/v1"

    CORS_ORIGINS: List[AnyHttpUrl] = []

    STORAGE_TYPE: str = "file"
    BASE_FILE_URL: str = "/uploads"
    BASE_FILE_PATH: str = "uploads"

    USE_SQLITE: bool = False
    SQLITE_URI: Optional[str]

    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    POSTGRES_URI: Optional[PostgresDsn] = None

    @field_validator("POSTGRES_URI", mode="before")
    @classmethod
    def posgres_uri(cls, v: Optional[str], info: ValidationInfo):
        user = info.data.get("POSTGRES_USER")
        password = info.data.get("POSTGRES_PASSWORD")
        server = info.data.get("POSTGRES_SERVER")
        db = info.data.get("POSTGRES_DB")

        if v:
            return v
        elif all([user, password, server, db]):
            return f"postgresql://{user}:{password}@{server}/{db}"

    class Config:
        env_file = ".env"


settings = Settings()
