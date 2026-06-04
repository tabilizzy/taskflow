import os
from sqlmodel import SQLModel, create_engine, Session, select
from typing import Optional, Generator
from dotenv import load_dotenv

load_dotenv()
# reads .env file into environment variables

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session




