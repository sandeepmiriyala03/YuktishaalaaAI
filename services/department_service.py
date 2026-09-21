from repository.department_repository import DepartmentRepository

class DepartmentService:

    @staticmethod
    def get_departments():
        return DepartmentRepository.get_departments()

    @staticmethod
    def get_department(department_id):
        return DepartmentRepository.get_department(department_id)

    @staticmethod
    def create_department(department):

        DepartmentRepository.create_department(
            department
        )

        return {
            "message":
                "Department Created"
        }

    @staticmethod
    def update_department(department_id, department):
        return DepartmentRepository.update_department(department_id, department)

    @staticmethod
    def delete_department(department_id):
        return DepartmentRepository.delete_department(department_id)