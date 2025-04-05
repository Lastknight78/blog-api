from typing import Any, Generic, Tuple, Type, TypeVar, Optional, get_args, get_origin
from pydantic import BaseModel
from sqlmodel import Session, or_, select
from sqlalchemy.sql.expression import BinaryExpression


Model = TypeVar("Model", bound=BaseModel)
ModelCreate = TypeVar("ModelCreate", bound=BaseModel)
ModelUpdate = TypeVar("ModelUpdate", bound=BaseModel)


class ActionClass(Generic[Model, ModelCreate, ModelUpdate]):
    _type_args: Optional[Tuple[Type[Model], Type[ModelCreate], Type[ModelUpdate]]] = None

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()

        orig_base = cls.__orig_bases__[0]
        origin = get_origin(orig_base)
        if origin is not ActionClass:
            raise TypeError(f"{cls.__name__} must subclass ActionClass with type parameters.")

        args = get_args(orig_base)
        if not all(args):
            raise TypeError(f"{cls.__name__} must provide all type parameters for ActionClass.")

        cls._type_args = args

    @classmethod
    def _get_type_args(cls) -> Tuple[Type[Model], Type[ModelCreate], Type[ModelUpdate]]:
        if not cls._type_args:
            raise TypeError(
                f"{cls.__name__} must subclass ActionClass with concrete type parameters like "
            )
        return cls._type_args

    def get(self, session: Session, *, id):
        ModelType = self._get_type_args()[0]
        return session.get(ModelType, id)

    def get_multi(self, session: Session, *, limit: int = 100, offset: int = 0):
        ModelType = self._get_type_args()[0]
        return session.exec(select(ModelType).offset(offset).limit(limit)).all()

    def get_by_all(self, session: Session, **dict):
        ModelType = self._get_type_args()[0]
        conditions = [getattr(ModelType, key) == value for key, value in dict.items()]
        return session.exec(select(ModelType).where(*conditions)).first()

    def get_by_any(self, session: Session, **dict):
        ModelType = self._get_type_args()[0]
        conditions = [getattr(ModelType, key) == value for key, value in dict.items()]
        return session.exec(select(ModelType).where(or_(*conditions))).first()

    def get_by_expression(self, session: Session, *exp: BinaryExpression):
        ModelType = self._get_type_args()[0]
        return session.exec(select(ModelType).where(*exp)).first()

    def multi_by_all(self, session: Session, *, limit: int = 100, offset: int = 0, **dict):
        ModelType = self._get_type_args()[0]
        conditions = [getattr(ModelType, key) == value for key, value in dict.items()]
        return session.exec(select(ModelType).where(*conditions).offset(offset).limit(limit)).all()

    def multi_by_any(self, session: Session, *, limit: int = 100, offset: int = 0, **dict):
        ModelType = self._get_type_args()[0]
        conditions = [getattr(ModelType, key) == value for key, value in dict.items()]
        return session.exec(
            select(ModelType).where(or_(*conditions)).offset(offset).limit(limit)
        ).all()

    def get_multi_by_expression(
        self, session: Session, *exp: BinaryExpression, limit: int = 100, offset: int = 0
    ):
        ModelType = self._get_type_args()[0]
        return session.exec(select(ModelType).where(*exp).offset(offset).limit(limit)).all()

    def create(self, session: Session, *, data: ModelCreate, update: dict[str, Any] = {}):
        ModelType = self._get_type_args()[0]
        data_dict = data.model_dump()
        data_dict.update(update)
        instance = ModelType(**data_dict)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    def update(
        self,
        session: Session,
        *,
        instance: Model,
        data: Optional[ModelUpdate] = None,
        update: dict[str, Any] = {},
    ):
        data_dict = data.model_dump(exclude_none=True, exclude_unset=True) if data else {}
        data_dict.update(update)

        for key, value in data_dict.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        session.add(instance)
        session.commit()
        session.refresh()

        return instance

    def delete(self, session: Session, *, id=id):
        instance = self.get(session, id=id)
        if instance:
            session.delete(instance)
            session.commit()
        return instance

    def delete_by_all(self, session: Session, **dict):
        instance = self.get_by_all(session, **dict)
        if instance:
            session.delete(instance)
            session.commit()
        return instance

    def delete_by_any(self, session: Session, **dict):
        instance = self.get_by_any(session, **dict)
        if instance:
            session.delete(instance)
            session.commit()
        return instance

    def delete_by_expression(self, session: Session, *exp: BinaryExpression):
        instance = self.get_by_expression(session, *exp)
        if instance:
            session.delete(instance)
            session.commit()
        return instance

    def random(self, **dict):
        return self._type_args[1](**dict)
