import os

from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("DATABASE_URL")
if not connection_string:
    raise RuntimeError("DATABASE_URL must be set in the environment")

engine = create_engine(
    connection_string,
    echo=True
)

