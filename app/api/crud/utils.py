import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class UniqueIdException(Exception):
    pass

class ItemNotFoundException(Exception):
    pass


def get_engine() -> Engine:
    host = os.environ["POSTGRES_HOST"]
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    database = os.environ["POSTGRES_DB"]

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:5432/{database}')

    return engine

engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
