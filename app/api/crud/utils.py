import os

from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class UniqueIdException(Exception):
    def __init__(self,message, class_str: str, id: str):
        super().__init__(message)
        self.message = message
        self.class_str = class_str
        self.id = id

class ItemNotFoundException(Exception):
    def __init__(self,message, class_str: str, id: str):
        super().__init__(message)
        self.message = message
        self.class_str = class_str
        self.id = id


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
