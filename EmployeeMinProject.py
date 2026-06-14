import json
from pathlib import Path
FILE = Path("DATA.json")
def load_data():
    if not FILE.exists():
        FILE.write_text("[]")
    return json.loads(FILE.read_text())

def save_data(employees):
    FILE.write_text(
        json.dumps(
            employees,
            indent=4
        )
    )
def create_employee():
    employees = load_data()
    name = input("Enter Name: ")
    salary = int(input("Enter Salary: "))
    age = int(input("Enter Age: "))
    employee = {
        "id": len(employees) + 1,
        "name": name,
        "salary": salary,
        "age": age
    }
    employees.append(employee)
    save_data(employees)
    print("✅ Employee Added")
def view_employees():
    employees = load_data()
    if not employees:
        print("No Employees Found")
        return
    print("\nEmployees")
    for emp in employees:
        print(
            f"ID: {emp['id']} | "
            f"Name: {emp['name']} | "
            f"Salary: {emp['salary']} | "
            f"Age: {emp['age']}"
        )
def update_employee():
    employees = load_data()
    emp_id = int(
        input("Enter Employee ID: ")
    )
    for emp in employees:
        if emp["id"] == emp_id:
            emp["name"] = input(
                "Enter New Name: "
            )
            emp["salary"] = int(
                input("Enter New Salary: ")
            )
            emp["age"] = int(
                input("Enter New Age: ")
            )
            save_data(employees)
            print("✅ Employee Updated")
            return
    print("❌ Employee Not Found")
def delete_employee():
    employees = load_data()
    emp_id = int(
        input("Enter Employee ID: ")
    )
    new_list = []
    for emp in employees:
        if emp["id"] != emp_id:
            new_list.append(emp)
    save_data(new_list)
    print("✅ Employee Deleted")
while True:
    print("\n===== Employee Manager =====")
    print("1. Create Employee")
    print("2. View Employees")
    print("3. Update Employee")
    print("4. Delete Employee")
    print("5. Exit")
    choice = input("Choose Option: ")
    if choice == "1":
       create_employee()
    elif choice == "2":
        view_employees()
    elif choice == "3":
        update_employee()
    elif choice == "4":
        delete_employee()
    elif choice == "5":
        print("Good Bye ")
        break
    else:
        print("Invalid Option")