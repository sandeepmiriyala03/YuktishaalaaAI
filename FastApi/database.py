import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection string (మీ డేటాబేస్ వివరాలను ఇక్కడ నవీకరించండి)
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/FASTAPI"

# 1. Engine Creation
engine = create_engine(DATABASE_URL)
_database_url = make_url(DATABASE_URL)


def get_raw_db_connection():
    connection_args = {
        "dbname": _database_url.database,
        "user": _database_url.username,
        "password": _database_url.password,
        "cursor_factory": RealDictCursor,
    }
    if _database_url.host:
        connection_args["host"] = _database_url.host
    if _database_url.port:
        connection_args["port"] = _database_url.port
    return psycopg2.connect(**connection_args)

# 2. Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base Class for Models
Base = declarative_base()

# 4. Dependency Helper for FastAPI Routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()