import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Determine if we should use SQLite (for local or Codex environments)
USE_SQLITE = os.environ.get("USE_SQLITE", "false").lower() == "true"

# Define the database URL based on the environment
DEFAULT_DATABASE_URL = (
    "postgresql://pgabackend_user:SD9jd5JEZPLt16kZIswcunk2MTCME5Qn@"
    "dpg-d188l0ogjchc73dtbti0-a.oregon-postgres.render.com/pgabackend"
)

if USE_SQLITE:
    # Use local SQLite DB (file-based or in-memory)
    DATABASE_URL = "sqlite:///./test.db"  # Use ":memory:" for non-persistent
else:
    # Use production DATABASE_URL from environment or fall back to default
    DATABASE_URL = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)

# Create SQLAlchemy engine with special args for SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create a session factory and base class for models
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
