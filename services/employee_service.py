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
    def get_employee(employee_id):
        return EmployeeRepository.get_employee(employee_id)

    @staticmethod
    def update_employee(employee_id, employee):
        return EmployeeRepository.update_employee(employee_id, employee)

    @staticmethod
    def delete_employee(employee_id):
        return EmployeeRepository.delete_employee(employee_id)

    @staticmethod
    def get_employees_sp():

        return EmployeeRepository.get_employees_sp()