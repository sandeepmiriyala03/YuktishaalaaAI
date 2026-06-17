from sqlalchemy import text
from database.db import engine

class EmployeeRepository:

    @staticmethod
    def create_employee(employee):

        with engine.connect() as conn:

            conn.execute(
                text("""
                    INSERT INTO Employees
                    (
                        Name,
                        Salary,
                        Age,
                        DepartmentId
                    )
                    VALUES
                    (
                        :name,
                        :salary,
                        :age,
                        :departmentId
                    )
                """),
                {
                    "name": employee.name,
                    "salary": employee.salary,
                    "age": employee.age,
                    "departmentId":
                        employee.departmentId
                }
            )

            conn.commit()

        return True