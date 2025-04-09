from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

bcrypt_scheme = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(secret: str) -> str:
    return bcrypt_scheme.hash(secret=secret)


def verify_password(secret: str, hash: str) -> bool:
    return bcrypt_scheme.verify(secret=secret, hash=hash)


def create_access_token(id: int, expiry=timedelta(days=7)):
    encode = {"id": id, "exp": expiry + datetime.now(timezone.utc)}
    return jwt.encode(encode, settings.SECRET_KEY, algorithm="HS256")
