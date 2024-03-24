from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists

from random_users.db_classes import Base

DB_URI = "sqlite:///random_users.db"


def create_db(db: str):
    engine = create_engine(db)
    if not database_exists(engine.url):
        Base.metadata.create_all(engine)


create_db(DB_URI)
