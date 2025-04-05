from sqlmodel import SQLModel
from sqlalchemy.engine import Engine
from app import models  # noqa: F401


def init_db(engine: Engine, create_table: bool = False):
    if create_table:
        SQLModel.metadata.drop_all(bind=engine)
        SQLModel.metadata.create_all(bind=engine)

    # with Session(bind=engine) as session:
    #     pass
