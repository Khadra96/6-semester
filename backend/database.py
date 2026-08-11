import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    postgres_database = os.getenv("POSTGRES_DB")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")

    if all([postgres_database, postgres_user, postgres_password]):
        DATABASE_URL = (
            f"postgresql+psycopg2://{postgres_user}:"
            f"{postgres_password}@localhost:5432/{postgres_database}"
        )
    else:
        DATABASE_URL = "sqlite:///./voltedge_test.db"

connection_arguments = {}

if DATABASE_URL.startswith("sqlite"):
    connection_arguments = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=connection_arguments,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def get_database_session():
    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()