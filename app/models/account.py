from sqlmodel import Field, Relationship
from .base import SchemaBase, ModelBase
from typing import TYPE_CHECKING, Optional
from .profile import ProfileRead

if TYPE_CHECKING:
    from .profile import Profile


class AccountBase(ModelBase):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    hash_password: str


class Account(AccountBase, table=True):
    profile: "Profile" = Relationship(
        back_populates="account", sa_relationship_kwargs={"uselist": False}
    )


class AccountRead(ModelBase):
    username: str
    email: str
    profile: Optional[ProfileRead]


class AccountCreate(SchemaBase):
    username: str
    email: str
    password: str


class AccountUpdate(SchemaBase):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
