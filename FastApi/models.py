from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, TIMESTAMP, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.expression import text

# Instantiate Base once for model inheritance
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
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text('now()'))

        # SQLAlchemy sets this value when the row is updated through the ORM.
    modified_Dt = Column(
                TIMESTAMP(timezone=True),
                nullable=True,
                onupdate=func.now(),
        )