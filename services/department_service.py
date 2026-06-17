from repository.department_repository import DepartmentRepository

class DepartmentService:

    @staticmethod
    def create_department(department):

        DepartmentRepository.create_department(
            department
        )

        return {
            "message":
                "Department Created"
        }