from sqlalchemy import text
from database.db import engine

class DepartmentRepository:

    @staticmethod
    def get_departments():
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    SELECT id,
                           DepartmentName AS departmentname,
                           Location AS location
                    FROM Departments
                """)
            ).mappings()
            return [
                {
                    "id": row["id"],
                    "departmentName": row["departmentname"],
                    "location": row["location"]
                }
                for row in result
            ]

    @staticmethod
    def get_department(department_id):
        with engine.connect() as conn:
            row = conn.execute(
                text("""
                    SELECT id,
                           DepartmentName AS departmentname,
                           Location AS location
                    FROM Departments
                    WHERE id = :department_id
                """),
                {"department_id": department_id}
            ).mappings().first()
            if not row:
                return None
            return {
                "id": row["id"],
                "departmentName": row["departmentname"],
                "location": row["location"]
            }

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

    @staticmethod
    def update_department(department_id, department):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    UPDATE Departments
                    SET DepartmentName = :department_name, Location = :location
                    WHERE id = :department_id
                """),
                {
                    "department_id": department_id,
                    "department_name": department.departmentName,
                    "location": department.location
                }
            )
            return result.rowcount > 0

    @staticmethod
    def delete_department(department_id):
        with engine.begin() as conn:
            result = conn.execute(
                text("DELETE FROM Departments WHERE id = :department_id"),
                {"department_id": department_id}
            )
            return result.rowcount > 0
    
    