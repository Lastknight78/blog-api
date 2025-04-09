from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.models import AccountRead, AccountCreate
from app.api import deps
from app.actions import account_action as aa


router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.post("/open", response_model=AccountRead, status_code=201)
def open_account(session: CommonSession, data: AccountCreate):
    if aa.get_by_all(session, email=data.email):
        raise HTTPException(status_code=401, detail="email already exists")
    if aa.get_by_all(session, username=data.username):
        raise HTTPException(status_code=401, detail="username already exists")
    return aa.create(session, data=data)
