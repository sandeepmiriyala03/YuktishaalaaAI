import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("DATABASE_URL", "sqlite:///./yuktishaalaa.db")

engine = create_engine(
    connection_string,
    connect_args={"check_same_thread": False} if connection_string.startswith("sqlite") else {},
    echo=False,
    future=True,
)


def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                DepartmentName VARCHAR(255) NOT NULL,
                Location VARCHAR(255) NOT NULL
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name VARCHAR(255) NOT NULL,
                Salary INTEGER NOT NULL,
                Age INTEGER NOT NULL,
                DepartmentId INTEGER NOT NULL
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL
            )
        """))


init_db()

