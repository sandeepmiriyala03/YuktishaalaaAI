class Employee:

    # Constructor
    def __init__(self, name, age, salary, status):
        print("Constructor Called")

        self.name = name
        self.age = age
        self.salary = salary
        self.status = status

    # Instance Method
    @staticmethod
    def display(self):
        print("\nEmployee Details")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Salary:", self.salary)
        print("Status:", "Active" if self.status else "Inactive")

    # Static Method
    @staticmethod
    def company():
        print("Company Name: OpenAI")


name = input("Enter employee name: ")
age = int(input("Enter employee age: "))
salary = float(input("Enter employee salary: "))
status = input("Enter employee status (Active/Inactive): ").lower() == "active"

# Constructor called automatically
Employee.display(Employee(name, age, salary, status))
Employee.company()