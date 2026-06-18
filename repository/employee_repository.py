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
                    "departmentId": employee.departmentId
                }
            )

            conn.commit()

        return True

    @staticmethod
    def get_employees():

        with engine.connect() as conn:

            result = conn.execute(
                text("""
                    SELECT
                        Id,
                        Name,
                        Salary,
                        Age,
                        DepartmentId
                    FROM Employees
                """)
            )

            employees = []

            for row in result:

                employees.append(
                    {
                        "id": row.Id,
                        "name": row.Name,
                        "salary": row.Salary,
                        "age": row.Age,
                        "departmentId": row.DepartmentId
                    }
                )

            return employees



    @staticmethod
    def get_employees_sp():

        with engine.connect() as conn:

            result = conn.execute(
                text("EXEC GetEmployees")
            )

            employees = []

            for row in result:

                employees.append(
                    {
                        "id": row.Id,
                        "name": row.Name,
                        "salary": row.Salary,
                        "age": row.Age,
                        "departmentId": row.DepartmentId
                    }
                )

            return employees