import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core import settings
from app.api.api_v1.api_routes import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router=api_router, prefix=f"{settings.API_V1_STR}")

if settings.STORAGE_TYPE == "file":
    if not os.path.exists(f"./{settings.BASE_FILE_PATH}"):
        os.mkdir(f"./{settings.BASE_FILE_PATH}")
    app.mount(
        settings.BASE_FILE_URL, StaticFiles(directory=settings.BASE_FILE_PATH), name="storage"
    )
