"""
Database utilities for ContentFlow AI API.
Handles SQLModel engine and session creation for Neon PostgreSQL.
"""
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

DATABASE_URL = os.environ.get("CFLOW_DB_URL", "sqlite:///./dev.db")
engine = create_engine(DATABASE_URL, echo=True)

@contextmanager
def get_session():
    """
    Provide a SQLModel session (context manager).
    Usage:
        with get_session() as session:
            ...
    """
    with Session(engine) as session:
        yield session

def init_db():
    """
    Create all tables (for initial dev/test only).
    """
    SQLModel.metadata.create_all(engine)
