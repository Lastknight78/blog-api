import logging
from app.db.init_db import init_db
from app.db.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DB Initialization")


def main():
    init_db(engine=engine, create_table=True)


if __name__ == "__main__":
    logger.info("Initializing db")
    main()
    logger.info("Database initialization completed")
