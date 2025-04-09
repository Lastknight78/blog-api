from typing import Any

from sqlmodel import Session
from .action import ActionClass
from app.models import Account, AccountCreate, AccountUpdate
from app.core.security import hash_password, verify_password
from faker import Faker

fake = Faker()


class AccountAction(ActionClass[Account, AccountCreate, AccountUpdate]):
    def create(self, session, *, data: AccountCreate, update: dict[str, Any] = {}):
        update = {}
        update["hash_password"] = hash_password(data.password)
        return super().create(session, data=data, update=update)

    def authenticate(self, session: Session, email: str, password: str, username: str):
        account = self.get_by_any(session, email=email, username=username)
        if not account or not verify_password(password, account.hash_password):
            return None
        return account

    def random(self, **dict):
        return AccountCreate(
            username=dict.get("username", fake.user_name()),
            email=dict.get("email", fake.email()),
            password=dict.get("password", fake.password()),
        )


account_action = AccountAction()
