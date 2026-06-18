from repository.employee_repository import EmployeeRepository

class EmployeeService:

    @staticmethod
    def create_employee(employee):

        EmployeeRepository.create_employee(employee)

        return {
            "message": employee.name + " Created"
        }

    @staticmethod
    def get_employees():

        return EmployeeRepository.get_employees()

    @staticmethod
    def get_employees_sp():

        return EmployeeRepository.get_employees_sp()