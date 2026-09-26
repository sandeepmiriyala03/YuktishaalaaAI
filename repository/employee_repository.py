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
                    SELECT id,
                           Name AS name,
                           Salary AS salary,
                           Age AS age,
                           DepartmentId AS departmentid
                    FROM Employees
                """)
            ).mappings()

            employees = []

            for row in result:

                employees.append(
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "salary": row["salary"],
                        "age": row["age"],
                        "departmentid": row["departmentid"]
                    }
                )

            return employees



    @staticmethod
    def get_employees_sp():

        if engine.dialect.name != "mssql":
            return EmployeeRepository.get_employees()

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

    @staticmethod
    def get_employee(employee_id):
        with engine.connect() as conn:
            row = conn.execute(
                text("""
                    SELECT id,
                           Name AS name,
                           Salary AS salary,
                           Age AS age,
                           DepartmentId AS departmentid
                    FROM Employees
                    WHERE id = :employee_id
                """),
                {"employee_id": employee_id}
            ).mappings().first()
            if not row:
                return None
            return {
                "id": row["id"],
                "name": row["name"],
                "salary": row["salary"],
                "age": row["age"],
                "departmentId": row["departmentid"]
            }

    @staticmethod
    def update_employee(employee_id, employee):
        with engine.begin() as conn:
            result = conn.execute(
                text("""
                    UPDATE Employees
                    SET Name = :name, Salary = :salary, Age = :age,
                        DepartmentId = :department_id
                    WHERE id = :employee_id
                """),
                {
                    "employee_id": employee_id,
                    "name": employee.name,
                    "salary": employee.salary,
                    "age": employee.age,
                    "department_id": employee.departmentId
                }
            )
            return result.rowcount > 0

    @staticmethod
    def delete_employee(employee_id):
        with engine.begin() as conn:
            result = conn.execute(
                text("DELETE FROM Employees WHERE id = :employee_id"),
                {"employee_id": employee_id}
            )
            return result.rowcount > 0