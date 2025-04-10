from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.db.session import engine
from app.core.security import verify_access_token
from app.core.config import settings
from app.actions import account_action as aa

oauth2_bearer = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


def get_session():
    with Session(engine) as session:
        yield session


def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_bearer)):
    account_id = verify_access_token(token)
    return aa.get(session, id=account_id)
