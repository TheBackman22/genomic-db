"""Database connection and session management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Connection string from environment, with sensible local default
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/genomics"
)

# Create engine - the core interface to the database
engine = create_engine(DATABASE_URL, echo=False)

# Session factory - creates new database sessions
SessionLocal = sessionmaker(bind=engine)


def get_session() -> Session:
    """Get a new database session.
    
    Usage:
        session = get_session()
        try:
            # do work
            session.commit()
        finally:
            session.close()
    
    Or as context manager:
        with get_session() as session:
            # do work
            session.commit()
    """
    return SessionLocal()
