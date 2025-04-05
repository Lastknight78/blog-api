from passlib.context import CryptContext

bcrypt_scheme = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(secret: str) -> str:
    return bcrypt_scheme.hash(secret=secret)


def verify_password(secret: str, hash: str) -> bool:
    bcrypt_scheme.verify(secret=secret, hash=hash)
