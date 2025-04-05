import os
from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from app.main import app
from app.api.deps import get_session
from app.db.init_db import init_db


# Create an in-memory SQLite test DB
if not os.path.exists("./tmp"):
    os.mkdir("./tmp")

DATABASE_URL = "sqlite:///./tmp/test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@pytest.fixture(scope="function")
def session() -> Generator:
    init_db(engine, create_table=True)
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(session) -> Generator:
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    yield TestClient(app)

    del app.dependency_overrides[get_session]
