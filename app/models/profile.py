from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship
from .base import ModelBase, SchemaBase

if TYPE_CHECKING:
    from .account import Account


class ProfileBase(ModelBase):
    account_id: int = Field(foreign_key="account.id")
    first_name: str
    last_name: str
    dob: Optional[date]
    avatar: Optional[str]


class Profile(ProfileBase, table=True):
    account: "Account" = Relationship(
        back_populates="profile", sa_relationship_kwargs={"uselist": False}
    )


class ProfileCreate(SchemaBase):
    first_name: str
    last_name: str
    dob: Optional[date]
    avatar: Optional[str]


class ProfileUpdate(SchemaBase):
    first_name: Optional[str]
    last_name: Optional[str]
    dob: Optional[date]
    avatar: Optional[str]


class ProfileRead(SchemaBase):
    id: int
    account_id: int
    first_name: str
    last_name: str
    dob: Optional[date]
    avatar: Optional[str]
