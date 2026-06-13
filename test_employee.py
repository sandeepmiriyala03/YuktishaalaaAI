import unittest
from Day1_p5 import Employee


class TestEmployee(unittest.TestCase):

    def test_employee_properties(self):
        emp1 = Employee()

        emp1.name = "Sandeep"
        emp1.age = 35
        emp1.salary = 100000
        emp1.status = "Active"

        self.assertEqual(emp1.name, "Sandeep")
        self.assertEqual(emp1.age, 35)
        self.assertEqual(emp1.salary, 100000)
        self.assertEqual(emp1.status, "Active")
        self.assertNotEqual(emp1.name, "John")
        self.assertNotEqual(emp1.age, 30)
        self.assertNotEqual(emp1.salary, 50000)
        self.assertNotEqual(emp1.status, "Inactive")


if __name__ == "__main__":
    unittest.main()