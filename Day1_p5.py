# Class = Blueprint/Template for creating Employee objects
class Employee:

    # Properties (variables) of Employee
    name = ""
    age = 0
    salary = 0
    status = True


# Object = Real Employee created from the Employee class
emp1 = Employee()

emp1.name = input("Enter employee name: ")
emp1.age = int(input("Enter employee age: "))
emp1.salary = float(input("Enter employee salary: "))
emp1.status = input("Enter employee status (Active/Inactive): ").lower() == "active"

# Display Employee details
print("\nEmployee Details")
print("Name:", emp1.name)
print("Age:", emp1.age)
print("Salary:", emp1.salary)
print("Status:", emp1.status)