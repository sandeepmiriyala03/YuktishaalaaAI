from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Numeric, String, TIMESTAMP, func
from sqlalchemy.sql.expression import text

from postgres_database import Base


class Test(Base):
    __tablename__ = "Test"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    Fname = Column(String(100), nullable=True)
    salary = Column(Numeric(10, 2), nullable=True)
    createdby = Column(String(50), nullable=False, default="System")
    createdat = Column(DateTime, default=datetime.now, nullable=False)
    modifiedby = Column(String(50), nullable=True)
    modifiedat = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=True)

    def __repr__(self):
        return f"<Test(Id={self.Id}, name='{self.name}', salary={self.salary})>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    modified_Dt = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())