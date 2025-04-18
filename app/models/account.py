from datetime import datetime
from sqlmodel import Field, Relationship
from .base import SchemaBase, ModelBase
from typing import TYPE_CHECKING, Optional
from .profile import ProfileRead
from .enum import BaseEnum

if TYPE_CHECKING:
    from .profile import Profile


class AccountRole(BaseEnum):
    admin = "admin"
    user = "user"


class AccountStatus(BaseEnum):
    active = "active"
    inactive = "inactive"
    banned = "banned"


class AccountBase(ModelBase):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hash_password: str
    role: AccountRole = Field(default=AccountRole.user)
    status: AccountStatus = Field(default=AccountStatus.active)
    last_login: Optional[datetime] = Field(nullable=True)
    # is_delete: Optional[bool] = Field(default=False)


class Account(AccountBase, table=True):
    profile: "Profile" = Relationship(
        back_populates="account", sa_relationship_kwargs={"uselist": False}
    )


class AccountRead(ModelBase):
    username: str
    email: str
    status: AccountStatus
    last_login: Optional[datetime]
    profile: Optional[ProfileRead]


class AccountCreate(SchemaBase):
    username: str
    email: str
    password: str


class AccountUpdate(SchemaBase):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
