from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.api import deps
from app.actions import account_action as aa
from app.core.security import create_access_token

router = APIRouter()


@router.post("/login")
def login(
    session: Session = Depends(deps.get_session), form_data: OAuth2PasswordRequestForm = Depends()
):
    account = aa.authenticate(session, form_data.username, form_data.password, form_data.username)
    if not account:
        raise HTTPException(status_code=401, detail="invalid email or password")
    if account.status.value == "banned":
        raise HTTPException(status_code=401, detail="account has been banned")
    account.last_login = datetime.now(timezone.utc)
    access_token = create_access_token(account.id)
    return {"access_token": access_token, "token_type": "bearer"}
