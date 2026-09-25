from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Test(Base):
    __tablename__ = 'Test'

    # Primary Key
    Id = Column(Integer, primary_key=True, autoincrement=True)

    # Core Fields
    name = Column(String(100), nullable=False)
    Fname = Column(String(100), nullable=True)  # Father's / First Name
    salary = Column(Numeric(10, 2), nullable=True)

    # Audit Trail Fields
    createdby = Column(String(50), nullable=False, default="System")
    createdat = Column(DateTime, default=datetime.utcnow, nullable=False)
    modifiedby = Column(String(50), nullable=True)
    modifiedat = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

    def __repr__(self):
        return f"<Test(Id={self.Id}, name='{self.name}', salary={self.salary})>"