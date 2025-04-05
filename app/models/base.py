from sqlmodel import SQLModel, Field
from datetime import datetime, date, timezone
from typing import Optional
from sqlalchemy.sql import func
from typing import ClassVar
from fastapi.encoders import jsonable_encoder


class SchemaBase(SQLModel):
    def jencode(self, exclude_none: bool = False):
        return jsonable_encoder(self, exclude_none=exclude_none)

    @classmethod
    def from_orm_(cls, obj, exclude_none: bool = False):
        return cls.model_validate(obj, from_attributes=True).jencode(exclude_none)

    model_config = {
        "use_enum_values": True,
        "from_attributes": True,
    }

    model_serializers: ClassVar[dict] = {
        datetime: lambda v: v.isoformat(),
        date: lambda v: v.isoformat(),
    }


class ModelBase(SchemaBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": func.now()},
    )
