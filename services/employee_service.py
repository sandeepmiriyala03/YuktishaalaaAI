from repository.employee_repository import EmployeeRepository

class EmployeeService:

    @staticmethod
    def create_employee(employee):

        EmployeeRepository.create_employee(
            employee
        )

        return {
            "message":
                employee.name + " Created"
        }