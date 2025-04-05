from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.models import AccountRead, AccountCreate
from app.api import deps
from app.actions import account_action as aa


router = APIRouter()

CommonSession = Annotated[Session, Depends(deps.get_session)]


@router.post("/open", response_model=AccountRead, status_code=201)
def open_account(session: CommonSession, data: AccountCreate):
    return aa.create(session, data=data)
