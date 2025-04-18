from typing import Annotated, TypeVar
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from app.models import AccountRead, AccountCreate, AccountUpdate, Account
from app.api import deps
from app.actions import account_action as aa

ModelUpdate = TypeVar("ModelUpdate", bound=BaseModel)

router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.post("/open", response_model=AccountRead, status_code=201)
def open_account(session: CommonSession, data: AccountCreate):
    if aa.get_by_all(session, email=data.email):
        raise HTTPException(status_code=401, detail="email already exists")
    if aa.get_by_all(session, username=data.username):
        raise HTTPException(status_code=401, detail="username already exists")
    return aa.create(session, data=data)


@router.get("/me", response_model=AccountRead)
def get_my_account(
    current_account: Account = Depends(deps.get_current_account),
):
    return current_account


@router.put("/update", response_model=AccountRead)
def update_my_account(
    session: CommonSession,
    data: AccountUpdate,
    current_account: Account = Depends(deps.get_current_account),
):
    print(data)
    if data.username:
        if data.username != current_account.username:
            exists = aa.get_by_all(session, username=data.username)
            if exists:
                raise HTTPException(status_code=400, detail="username already exists")
            aa.update(session, data=data, instance=current_account)
    if data.email:
        if data.email != current_account.email:
            exists = aa.get_by_all(session, email=data.email)
            if exists:
                raise HTTPException(status_code=400, detail="email already exists")
            aa.update(session, data=data, instance=current_account)
    return current_account


@router.delete("/delete/me", status_code=200)
def delete_my_account(
    session: CommonSession,
    current_account: Account = Depends(deps.get_current_account),
):
    return aa.delete(session, id=current_account.id)


@router.get("/{account_id}", response_model=AccountRead)
def get_account(
    session: CommonSession,
    account_id: int,
    current_account: Account = Depends(deps.get_current_account),
):
    account = aa.get_by_all(session, id=account_id)
    if not account:
        raise HTTPException(status_code=404, detail="account not found")
    return account
