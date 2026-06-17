from sqlalchemy import text
from database.db import engine

class DepartmentRepository:

    @staticmethod
    def create_department(department):

        with engine.connect() as conn:

            conn.execute(
                text("""
                    INSERT INTO Departments
                    (
                        DepartmentName,
                        Location
                    )
                    VALUES
                    (
                        :departmentName,
                        :location
                    )
                """),
                {
                    "departmentName":
                        department.departmentName,

                    "location":
                        department.location
                }
            )

            conn.commit()

        return True