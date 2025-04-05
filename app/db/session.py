from sqlmodel import create_engine
from app.core import settings

if settings.USE_SQLITE:
    engine = create_engine(
        url=settings.SQLITE_URI,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    engine = create_engine(url=settings.POSTGRES_URI, pool_pre_ping=True)
