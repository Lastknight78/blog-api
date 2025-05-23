from fastapi.testclient import TestClient
from sqlmodel import Session
from app.actions import account_action as aa
from app.core import settings
from app.models import AccountRead
from app.tests.utils.auth import create_account_with_headers


def test_open_account(client: TestClient, session: Session):
    data = aa.random()

    response = client.post(f"{settings.API_V1_STR}/accounts/open", json=data.model_dump())
    assert response.status_code == 201
    content = response.json()
    retrieved_data = aa.get(session, id=content["id"])
    assert content == AccountRead.from_orm_(retrieved_data)


def test_open_account_email_exists(client: TestClient, session: Session):
    account = aa.create(session, data=aa.random())
    data = aa.random(email=account.email).model_dump()
    response = client.post(f"{settings.API_V1_STR}/accounts/open", json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "email already exists"


def test_open_account_username_exists(client: TestClient, session: Session):
    account = aa.create(session, data=aa.random())
    data = aa.random(username=account.username).model_dump()
    response = client.post(f"{settings.API_V1_STR}/accounts/open", json=data)
    assert response.status_code == 401
    assert response.json()["detail"] == "username already exists"


def test_get_account(session: Session, client: TestClient):
    _, headers = create_account_with_headers(session, client)
    response = client.get(f"{settings.API_V1_STR}/accounts/10000", headers=headers)

    assert response.status_code == 404
    assert response.json()["detail"] == "account not found"


def test_get_my_account_exists(session: Session, client: TestClient):
    _, headers = create_account_with_headers(session, client)
    response = client.get(
        f"{settings.API_V1_STR}/accounts/me",
        headers=headers,
    )

    assert response.status_code == 200


def test_delete_account(session: Session, client: TestClient):
    _, headers = create_account_with_headers(session, client)
    response = client.delete(
        f"{settings.API_V1_STR}/accounts/delete/me",
        headers=headers,
    )
    assert response.status_code == 200


def test_check_if_email_exists(session: Session, client: TestClient):
    _, headers = create_account_with_headers(session, client)
    account = aa.create(session, data=aa.random())
    data = {"email": account.email}
    response = client.put(
        f"{settings.API_V1_STR}/accounts/update",
        headers=headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "email already exists"


def test_check_if_username_exists(session: Session, client: TestClient):
    _, headers = create_account_with_headers(session, client)
    account = aa.create(session, data=aa.random())
    data = {"username": account.username}
    response = client.put(
        f"{settings.API_V1_STR}/accounts/update",
        headers=headers,
        json=data,
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "username already exists"
