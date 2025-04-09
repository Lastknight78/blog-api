import secrets
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from pydantic import field_validator, ValidationInfo


class Settings(BaseSettings):
    PROJECT_NAME: str
    PROJECT_VERSION: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_hex(32)

    CORS_ORIGINS: List[AnyHttpUrl] = []

    STORAGE_TYPE: str = "file"
    BASE_FILE_URL: str = "/uploads"
    BASE_FILE_PATH: str = "uploads"

    USE_SQLITE: bool = False
    SQLITE_URI: Optional[str] = None

    POSTGRES_USER: str = "localhost"
    POSTGRES_PASSWORD: str = "1234"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_DB: str = "localhost"

    POSTGRES_URI: Optional[str] = None

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
