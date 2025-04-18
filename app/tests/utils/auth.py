from typing import Any
from app.core.config import settings
from app.actions import account_action as aa
from sqlmodel import Session
from fastapi.testclient import TestClient


def create_account_with_headers(session: Session, client: TestClient, **data: dict[str, Any]):
    data = aa.random(**data)
    account = aa.create(session, data=data)
    response = client.post(
        f"{settings.API_V1_STR}/login", data={"username": data.email, "password": data.password}
    )
    return account, {"Authorization": f"bearer {response.json()['access_token']}"}
