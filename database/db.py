import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("DATABASE_URL", "sqlite:///:memory:")

engine = create_engine(
    connection_string,
    echo=True
)

