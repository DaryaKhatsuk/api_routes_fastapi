from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://Admin:5947@localhost/dbname"
# engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
