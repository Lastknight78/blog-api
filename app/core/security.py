from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings
from app.models import TokenData

bcrypt_scheme = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(secret: str) -> str:
    return bcrypt_scheme.hash(secret=secret)


def verify_password(secret: str, hash: str) -> bool:
    return bcrypt_scheme.verify(secret=secret, hash=hash)


def create_access_token(id: int, expiry=timedelta(days=7)):
    encode = {"id": id, "exp": expiry + datetime.now(timezone.utc)}
    return jwt.encode(encode, settings.SECRET_KEY, algorithm="HS256")


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
    token = TokenData(payload.get("id"))
    return token
