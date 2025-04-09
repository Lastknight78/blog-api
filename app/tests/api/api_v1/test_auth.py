from fastapi.testclient import TestClient
from pytest import Session
from app.actions import account_action as aa
import pytest
from app.core.config import settings


@pytest.mark.parametrize("value", ["dammy", "dammy@gmail.com"])
def test_login(client: TestClient, session: Session, value: str):
    aa.create(session, data=aa.random(username="dammy", email="dammy@gmail.com", password="123"))
    response = client.post(
        url=f"{settings.API_V1_STR}/login", data={"username": value, "password": "123"}
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
