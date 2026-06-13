# ABC = Abstract Base Class
from abc import ABC, abstractmethod

# dataclass automatically creates __init__()
from dataclasses import dataclass


# Abstract Base Class (cannot create object directly)
@dataclass
class Employee(ABC):

    # Properties
    name: str
    age: int
    salary: float
    status: bool

    # Abstract Method
    # Child classes MUST implement this method
    @abstractmethod
    def display(self):
        pass

    # Static Method
    # Can be called without creating an object
    @staticmethod
    def company():
        print("Company Name: OpenAI")


# Child Class inheriting Employee
class PermanentEmployee(Employee):

    # Method Override
    def display(self):

        # self = current object
        print("\nEmployee Details")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Salary:", self.salary)
        print("Status:", "Active" if self.status else "Inactive")


# User Input
name = input("Enter employee name: ")
age = int(input("Enter employee age: "))
salary = float(input("Enter employee salary: "))
status = input("Enter employee status (Active/Inactive): ").lower() == "active"

# Object Creation
# dataclass automatically generated __init__()
emp1 = PermanentEmployee(name, age, salary, status)

# Call Instance Method
emp1.display()

# Call Static Method
Employee.company()