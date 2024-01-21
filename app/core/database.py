import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from .config import env_vars


DATABASE_URL = env_vars.DATABASE_URL


engine = create_engine(DATABASE_URL, connect_args={}, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        logging.info("Connection to PostgreSQL database server is established")
        yield db
    finally:
        db.close()
