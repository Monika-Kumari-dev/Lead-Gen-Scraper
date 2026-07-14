"""
Database setup using SQLAlchemy.

Dev: SQLite (leads.db, zero setup).
Prod: swap DATABASE_URL to a MySQL connection string, e.g.:
    "mysql+pymysql://user:password@localhost/leads_db"
No other code changes needed since we use the SQLAlchemy ORM.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./leads.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency - yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
