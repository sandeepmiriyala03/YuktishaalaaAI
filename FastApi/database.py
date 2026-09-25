from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL connection string (మీ డేటాబేస్ వివరాలను ఇక్కడ నవీకరించండి)
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/FASTAPI"

# 1. Engine Creation
engine = create_engine(DATABASE_URL)

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