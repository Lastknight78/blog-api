from fastapi.testclient import TestClient
from sqlmodel import Session
from app.actions import account_action as aa
from app.core import settings
from app.models import AccountRead


def test_open_account(client: TestClient, session: Session):
    data = aa.random()

    response = client.post(f"{settings.API_V1_STR}/accounts/open", json=data.model_dump())
    assert response.status_code == 201
    content = response.json()
    retrieved_data = aa.get(session, id=content["id"])
    assert content == AccountRead.from_orm_(retrieved_data)
